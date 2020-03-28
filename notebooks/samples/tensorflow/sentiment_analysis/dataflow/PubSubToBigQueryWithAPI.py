# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A streaming python pipeline to read in PubSub tweets and perform
classification using Prediction API"""

import argparse
import datetime
import json
import logging
import numpy as np
import os
import socket
import subprocess

import apache_beam as beam
import apache_beam.transforms.window as window

from apache_beam.io.gcp.bigquery_tools import parse_table_schema_from_json
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import PipelineOptions

from apache_beam.transforms.util import BatchElements, GroupIntoBatches

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.api_core import retry
from google.api_core import exceptions
from google.cloud import language_v1
from google.cloud.language_v1 import enums

TIMEOUT_IN_SEC = 60 * 2 # 2 minutes timeout limit
socket.setdefaulttimeout(TIMEOUT_IN_SEC)

PROJECT_ID = os.getenv('PROJECT_ID')


def get_sentiment(instances_content):
    """Analyzing Sentiment in a String

    Args:
        text_content The text content to analyze
    """
    scores = []
    client = language_v1.LanguageServiceClient()
    encoding_type = enums.EncodingType.UTF8
    language = 'en'
    type_ = enums.Document.Type.PLAIN_TEXT
    for content in instances_content:
        content = content.encode('utf-8') if isinstance(content,
                                                        unicode) else str(
            content)
        document = {'content': content, 'type': type_, 'language': language}
        try:
            response = client.analyze_sentiment(document,
                                                encoding_type=encoding_type,
                                                timeout=30,
                                                retry=retry.Retry(deadline=60))
            # Get overall sentiment of the input document
            if response.document_sentiment.score:
                scores.append(response.document_sentiment.score)
            else:
                scores.append(-1)
                logging.error(
                    'Document sentiment score not found for {}'.format(content))
        except exceptions.GoogleAPICallError as e:
            logging.exception(e)
        except exceptions.RetryError as e:
            logging.exception(e)
        except ValueError as e:
            logging.exception(e)
    return scores


def prediction_helper(messages):
    """Processes PubSub messages and calls AI Platform prediction.

    :param messages:
    :return:
    """
    # Handle single string.
    if not isinstance(messages, list):
        messages = [messages]

    # Messages from PubSub are JSON strings
    instances = list(map(lambda message: json.loads(message), messages))
    # Estimate the sentiment of the 'text' of each tweet
    scores = get_sentiment(
        [instance['text'] for instance in instances if instance.get('text')])

    if len(scores) == len(instances):
        for i, instance in enumerate(instances):
            logging.info('Processed {} instances.'.format(len(instances)))
            instance['sentiment'] = scores[i]
        return instances
    else:
        logging.error('Invalid scores {} instances {}'.format(len(scores),
                                                              len(instances)))
        logging.error(instances)
        return


class GroupWindowsIntoBatches(beam.PTransform):
    """A composite transform that groups Pub/Sub messages based on publish
    time and outputs a list of dictionaries, where each contains one message
    and its publish timestamp.
    """

    def __init__(self, window_size):
        # Convert minutes into seconds.
        self.window_size = int(window_size * 60)

    def expand(self, pcoll):
        return (
            pcoll
            # Assigns window info to each Pub/Sub message based on its
            # publish timestamp.
            | "Window into Fixed Intervals"
            >> beam.WindowInto(window.FixedWindows(self.window_size))
            | "Add timestamps to messages" >> beam.ParDo(AddTimestamps())
            # Use a dummy key to group the elements in the same window.
            # Note that all the elements in one window must fit into memory
            # for this. If the windowed elements do not fit into memory,
            # please consider using `beam.util.BatchElements`.
            # https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.util.html#apache_beam.transforms.util.BatchElements
            | "Add Dummy Key" >> beam.Map(lambda elem: (None, elem))
            | "Groupby" >> beam.GroupByKey()
            | "Abandon Dummy Key" >> beam.MapTuple(lambda _, val: val)
        )


class AddTimestamps(beam.DoFn):
    def process(self, element, publish_time=beam.DoFn.TimestampParam):
        """Processes each incoming windowed element by extracting the Pub/Sub
        message and its publish timestamp into a dictionary. `publish_time`
        defaults to the publish timestamp returned by the Pub/Sub server. It
        is bound to each element by Beam at runtime.
        """

        yield {
            "message_body": element.decode("utf-8"),
            "publish_time": datetime.datetime.utcfromtimestamp(
                float(publish_time)
            ).strftime("%Y-%m-%d %H:%M:%S.%f"),
        }

def run(args, pipeline_args=None):
    """Executes Pipeline.

    :param args:
    :param pipeline_args:
    :return:
    """
    """Build and run the pipeline."""
    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True
    )
    pipeline_options.view_as(StandardOptions).runner = args.runner
    # Run on Cloud DataFlow by default
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.project = PROJECT_ID
    google_cloud_options.job_name = 'pubsub-api-bigquery'
    google_cloud_options.staging_location = args.staging_location
    google_cloud_options.temp_location = args.temp_location
    google_cloud_options.region = args.region

    p = beam.Pipeline(options=pipeline_options)

    lines = p | 'read in tweets' >> beam.io.ReadFromPubSub(
        topic=args.input_topic,
        with_attributes=False,
        id_label='tweet_id')    # TODO: Change to PubSub id.

    # Window them, and batch them into batches. (Not too large)
    output_tweets = (lines | 'assign window key' >> beam.WindowInto(
        window.FixedWindows(args.window_size))
                     | 'batch into n batches' >> BatchElements(
            min_batch_size=args.min_batch_size,
            max_batch_size=args.max_batch_size)
                     | 'predict sentiment' >> beam.FlatMap(
            lambda messages: prediction_helper(messages))
                     )

    # Make explicit BQ schema for output tables:
    bq_schema_json = {"fields": [{"name": "id", "type": "STRING"},
                                 {"name": "text", "type": "STRING"},
                                 {"name": "user_id", "type": "STRING"},
                                 {"name": "sentiment", "type": "FLOAT"},
                                 {"name": "posted_at", "type": "TIMESTAMP"},
                                 {"name": "favorite_count", "type": "INTEGER"},
                                 {"name": "retweet_count", "type": "INTEGER"},
                                 {"name": "media", "type": "STRING"},
                                 ]}
    bq_schema = parse_table_schema_from_json(json.dumps(bq_schema_json))

    # Write to BigQuery
    output_tweets | 'store twitter posts' >> beam.io.WriteToBigQuery(
        table=args.bigquery_table,
        dataset=args.bigquery_dataset,
        schema=bq_schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        project=PROJECT_ID
    )
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-topic',
        help='The Cloud Pub/Sub topic to read from.\n'
             'projects/<PROJECT_NAME>/topics/<TOPIC_NAME>',
        required=True
    )
    parser.add_argument(
        '--region',
        help='The DataFlow region',
        default='us-central1'
    )
    parser.add_argument(
        '--staging-location',
        help='The DataFlow staging location',
        default='gs://<bucket_name>/staging/',
        required=True
    )
    parser.add_argument(
        '--temp-location',
        help='The DataFlow temp location',
        default='gs://<bucket_name>/tmp/',
        required=True
    )
    parser.add_argument(
        '--bigquery-dataset',
        help='BigQuery dataset',
        required=True
    )
    parser.add_argument(
        '--bigquery-table',
        help='BigQuery OutPut table',
        required=True
    )
    parser.add_argument(
        '--window-size',
        type=int,
        default=60,
        help="Output file's window size in number of seconds",
    )
    parser.add_argument(
        '--min-batch-size',
        type=int,
        default=1,
        help='Min batch size for Windowing',
    )
    parser.add_argument(
        '--max-batch-size',
        type=int,
        default=100,
        help='Min batch size for Windowing',
    )
    parser.add_argument(
        '--runner',
        type=str,
        default='DataflowRunner',
        help='DataFlow running mode',
    )
    known_args, pipeline_args = parser.parse_known_args()

    run(
        known_args,
        pipeline_args
    )

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the \"License\");
# you may not use this file except in compliance with the License.\n",
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an \"AS IS\" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import numpy as np

from transformers import (
    AutoTokenizer,
    EvalPrediction,
    Trainer,
    TrainingArguments,
    default_data_collator
)

from trainer import model, metadata, utils


def compute_metrics(p: EvalPrediction):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    preds = np.argmax(preds, axis=1)
    return {"accuracy": (preds == p.label_ids).astype(np.float32).mean().item()}


def train(args, model, train_dataset, test_dataset):
    """Create the training loop for one epoch. Read the data from the
     dataloader, calculate the loss, and update the DNN. Lastly, display some
     statistics about the performance of the DNN during training.

    Args:
      sequential_model: The neural network that you are training, based on
      nn.Module
      train_loader: The training dataset
      criterion: The loss function used during training
      optimizer: The selected optmizer to update parameters and gradients
      epoch: The current epoch that the training loop is on
    """
    
    tokenizer = AutoTokenizer.from_pretrained(
        metadata.PRETRAINED_MODEL_NAME,
        use_fast=True,
    )
    
    training_args = TrainingArguments(
        evaluation_strategy="epoch",
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.num_epochs,
        weight_decay=args.weight_decay,
        output_dir=os.path.join("/tmp", args.model_name)
    )
    
    trainer = Trainer(
        model,
        training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        data_collator=default_data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    
    trainer.train()
    return trainer


def run(args):
    """Load the data, train, evaluate, and export the model for serving and
     evaluating.

    Args:
      args: experiment parameters.
    """
    # Open our dataset
    train_dataset, test_dataset = utils.load_data(args)

    label_list = train_dataset.unique("label")
    num_labels = len(label_list)
    
    # Create the model, loss function, and optimizer
    text_classifier = model.create(num_labels=num_labels)
    
    # Train / Test the model
    trainer = train(args, text_classifier, train_dataset, test_dataset)

    # Export the trained model
    trainer.save_model(os.path.join("/tmp", args.model_name))

    # Save the model to GCS
    if args.job_dir:
        utils.save_model(args)

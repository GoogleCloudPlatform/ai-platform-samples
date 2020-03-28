## Google Cloud Streaming Pipeline

### Overview

This Python script collects information from Twitter stream and
pushes Tweets to PubSub.
The Twitter API gives developers access to most of Twitter’s functionality. 
You can use the API to read and write information related to Twitter 
entities such as tweets, users, and trends.

Technically, the API exposes dozens of HTTP endpoints related to:

  - Tweets
  - Retweets
  - Likes
  - Direct messages
  - Favorites
  - Trends
  - Media

We will use [Tweepy](https://www.tweepy.org/), it provides a way to invoke 
Twitter API endpoints without dealing with low-level details.

### Configuration

Install dependencies in `requirements.txt` file Create a Twitter
developer account and get Authentication information
[here](https://developer.twitter.com/) 

Twitter API requires that all requests use OAuth to authenticate. You
need to:
  - Apply for a Twitter Developer Account
  - Create an application
  - Create the Authentication credentials
  
Once you create the authentication credentials you will be able to use
the API. These credentials are the following text strings:

  - Consumer key
  - Consumer secret
  - Access token
  - Access secret

### Google Cloud information

```
export PROJECT_ID=""
export PUBSUB_TOPIC=""
```

### Twitter authentication

Make sure you create the Twitter information in advanced.


```
export CONSUMER_KEY=""
export CONSUMER_SECRET=""
export ACCESS_TOKEN=""
export ACCESS_TOKEN_SECRET=""
```

### Running application
 
You can build Docker container or run the Python script directly. In
this case we will show you how to build and run the Docker container.

### Build container

```
docker build -t twitter-listener . --no-cache
```

### Run container

Authenticate via Google Cloud

```
export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
```

```
docker run -d --name="twitter-listener" --hostname="twitter-listener" 
    -v /usr/local/src/newsml/conf/credentials/key.json:/config \
    -e PROJECT_ID="" \
    -e PUBSUB_TOPIC="" \ 
    -e CONSUMER_KEY="" \
    -e CONSUMER_SECRET="" \ 
    -e ACCESS_TOKEN="" \
    -e ACCESS_TOKEN_SECRET="" \ 
    -e GOOGLE_APPLICATION_CREDENTIALS="/config" \
    -v ~/.config:/root/.config twitter-listener \
    --restart on-failure:5
```

Verify tweets are being captured

```
docker logs -f twitter-listener
```

References:
https://realpython.com/twitter-bot-python-tweepy/#reader-comments

#!/usr/bin/env python
# MagicGoolsbee/bot.py

import tweepy
import logging
from config import create_api
import time
import requests
from links import links
import random
import re

GOOLSBALL_TEXT = " You shake the Magic Goolsball aaaand..."
GOOLSBALL_USERNAME = "@MagicGoolsbee"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_random_image():
    rand = random.randint(0, 71)
    logger.info("Random number = " + str(rand))
    url = links[rand]
    logger.info("Random URL is " + url)
    return url


def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is None:  # Respond to top level tweets
            logger.info("Answering to " + tweet.user.screen_name)
            logger.info("Tweet Text " + tweet.full_text)
            image = get_image(api, get_random_image())
            api.update_status(
                status="@" + tweet.user.screen_name + GOOLSBALL_TEXT,
                in_reply_to_status_id=tweet.id, media_ids=[image.media_id_string]
            )
        else:  # respond to reply tweets

            test_string = tweet.full_text.split(" ", 1)
            test_string2= tweet.full_text
            logger.info("test string 1= " + test_string[0] + " "+ test_string[1])
            logger.info("test string 2= " + test_string2)
            if test_string[0] == GOOLSBALL_USERNAME:
                test_string2 = test_string[1]
            logger.info("after if test string 2= " + test_string2)
            # if a second mention occurs that means its in the main text and should be responded to
            if GOOLSBALL_USERNAME in test_string2:
                logger.info("Answering to " + tweet.user.screen_name)
                logger.info("Tweet Text " + test_string2)
                image = get_image(api, get_random_image())
                api.update_status(
                    status="@" + tweet.user.screen_name + GOOLSBALL_TEXT,
                    in_reply_to_status_id=tweet.id, media_ids=[image.media_id_string]
                )
    return new_since_id


def get_image(api, url):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        media = api.media_upload(filename)
    else:
        logger.info("Unable to download image")
    return media


def main():
    api = create_api()
    count=0
    tweet = tweepy.Cursor(api.mentions_timeline).items().next()
    since_id=tweet.id
    logger.info("SinceID = " + str(since_id))
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()

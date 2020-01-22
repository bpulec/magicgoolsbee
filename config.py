# magicgoolsbee/config.py
import tweepy
import logging
from secrets import *

logger = logging.getLogger()


def create_api():
    consumer_key = C_KEY
    consumer_secret = C_SECRET
    access_token = A_TOKEN
    access_token_secret = A_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

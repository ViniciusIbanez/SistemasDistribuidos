import snscrape.modules.twitter as sntwitter
from datetime import timedelta ,datetime
import argparse
import time
import logging

def retrieve_arguments():
    parser = argparse.ArgumentParser(description='Retrives info to extract tweets')
    parser.add_argument('--u', type=str , help='username') 
    parser.add_argument('--n', type=int , help='count of tweets to extract') 
    args = parser.parse_args()

    return args


def retrieve_tweets(args):

    maxTweets = args.n
    user = args.u

    today = datetime.now().strftime("%Y-%m-%d")
    since  =  (datetime.now() - timedelta(days=365*2)).strftime("%Y-%m-%d")

    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:@{user} + since:{since} until:{today}-filter:replies').get_items()):
        if i > maxTweets :
            break
        logging.info(f'User: {user} Tweet_count: {i} Tweet_content: {tweet.content}\n')


def run():
    args = retrieve_arguments()
    retrieve_tweets(args)
    return True 

run()

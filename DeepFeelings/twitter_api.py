import os
from dotenv import load_dotenv
import time
import requests
import tweepy
from datetime import datetime, timedelta
import gcsfs
import pandas as pd


def get_user_id(user_name, bearer_token):
    '''returns the twitter id given a user name'''

    url = f'https://api.twitter.com/2/users/by/username/{user_name}'
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers = headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()['data']['id']


def get_lastest_tweets(user_name, n_tweets):
    '''returns a df with a column dates and a column text with the tweets
        user_name = the user name on twitter
        n_tweets = number of tweets to retrieve
        note: it will return at least n_tweets but it can return around 10 more'''

    # Total number of tweets we collected from the loop
    total_tweets = 0

    # Inputs
    flag = True
    next_token = None

    # Load token and get user id
    load_dotenv()
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    user_id = get_user_id(user_name, bearer_token)

    # Dates
    start_time = datetime.now() - timedelta(hours=3)
    end_time = datetime.now()

    # Dictionary to store the data
    data = {'date': [], 'text': []}

    # tweepy client
    client = tweepy.Client(bearer_token)

    # Check if flag is true
    while flag:

        response = client.get_users_mentions(id=user_id, start_time=start_time, end_time=end_time)
        result_count = response.meta['result_count']

        if 'next_token' in response.meta and total_tweets<n_tweets:
            # Save the token to use for next call
            next_token = response.meta['next_token']
            print("Next Token: ", next_token)

            if result_count is not None and result_count > 0 and next_token is not None:
                print("Start Date: ", start_time)
                for tweet in response.data:
                    text = tweet['text'].replace('\n', ' ')
                    data['date'].append(end_time)
                    data['text'].append(text)
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(2)

        # If no next token exists
        else:
            '''if result_count is not None and result_count > 0:
                print("-------------------")
                print("Start Date: ", start_time)
                for tweet in response.data:
                    text = tweet['text'].replace('\n', ' ')
                    data['date'].append(end_time)
                    data['text'].append(text)
                    total_tweets += result_count'''
            print("Total # of Tweets added: ", total_tweets)
            print("-------------------")
            time.sleep(2)

            # Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            next_token = None
        time.sleep(2)
    print("Total number of results: ", total_tweets)

    return pd.DataFrame.from_dict(data)

if __name__=='__main__':
    df = get_lastest_tweets('Apple', 10)
    print(f'First tweet: {df["text"][0]}')

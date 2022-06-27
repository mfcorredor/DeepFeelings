import os
from dotenv import load_dotenv
import time
import requests
import tweepy
from datetime import datetime, timedelta
import pandas as pd


def get_user_id(user_name, bearer_token):
    """
    Returns the twitter id given a user name.
    If user name doesn't exist, it returns ''
        user_name (str): user name on Twitter
        bearer_token (str): token to acces Twitter API
    """

    url = f'https://api.twitter.com/2/users/by/username/{user_name}'
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers = headers)
    if response.status_code != 200:
        return ''
    return response.json()['data']['id']


def get_tweets(user_name, n_tweets=500, verbose=True):
    """
    Gets the tweets that mentions a user name with dates
        user_name (str): the user name on twitter
        n_tweets (int): number of tweets to retrieve
        verbose (bool): shows commets of the retrieval
    Returns a DataFrame with a column dates and a column text with the tweets.
    If user name doesn't exist, it returns ''
    It will return at least n_tweets but it can return around 10 more
    """

    # Load token and check user name
    load_dotenv()
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    user_id = get_user_id(user_name, bearer_token)
    if user_id == '':
        return ''

    # Total number of tweets we collected from the loop
    total_tweets = 0

    # Inputs
    flag = True
    next_token = None

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
                if verbose==True:
                    print("Total # of Tweets added: ", total_tweets)
                    print("-------------------")
                time.sleep(1)

        # If no next token exists
        else:
            if verbose==True:
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")

            # Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            next_token = None
    if verbose==True:
        print("Total number of results: ", total_tweets)

    return pd.DataFrame.from_dict(data)

if __name__=='__main__':
    df = get_tweets('Apple', 10)
    print(f'First tweet: {df["text"][0]}')

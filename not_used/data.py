import pandas as pd
from amzwbscr_selenium import scrape_amz
from twitter_api import get_lastest_tweets

def get_data(ls_product_id, user_name, n_tweets=100):
    '''Get the data from the twitter api and amazon web scraping and join to a df.
        Returns a df with 3 columns: country, dates and text with the tweets and amazon product reviews.
        ls_product_id = is a list of amazon product ids of the enterprise
        user_name = the user name of the enterprice on twitter
        n_tweets = number of tweets to retrieve (note: it will return at least n_tweets
        but it can return around 10 more'''

    df = pd.DataFrame()

    for i in ls_product_id:
        product_reviews = scrape_amz(i)
        df = pd.concat([df,product_reviews])

    tweets = get_lastest_tweets(user_name, n_tweets)

    return pd.concat([df,tweets])

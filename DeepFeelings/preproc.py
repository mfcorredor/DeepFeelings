import pandas as pd
import re
import string
import numpy as np
import emoji
from nltk.corpus import words
from amzwbscr_selenium import scrape_amz
from twitter_api import get_lastest_tweets

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

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

def preproc(data):

    #data = get_data(ls_product_id, user_name, n_tweets)

    # Remove user names
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                                if not word.startswith("@")]))

    #Remove emojis
    data.text = data.text.apply(lambda x: remove_emoji(x))

    #Make text lowercase
    data.text = data.text.apply(lambda x: x.lower())

    #remove text in square brackets
    data.text = data.text.apply(lambda x: re.sub(r"[\()]", "", x))

    #remove links
    data.text = data.text.apply(lambda x: re.sub('https?://\S+|www\.\S+', '', x))

    #remove some punctuation
    data.text = data.text.apply(lambda x: re.sub('<*>+', '', x))

    #containing numbers
    #data.text = data.text.apply(lambda x: re.sub('\n', '', x))

    #remove numbers
    #data.text = data.text.apply(lambda x: re.sub('\w*\d\w*', '', x))

    #remove numbers
    #data.text = ''.join([i for i in data.text if not i.isdigit()])

    # Remove user names
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                                if not word.startswith("@")]))

    # Remove non english words
    en_words = set(words.words())
    data.text = data.text.apply(lambda x: " ".join(w for w in x.split()\
                                if w in en_words))
    data.text.replace('', np.nan, inplace=True)
    data.dropna(subset=['text'], inplace=True)

    # Remove strings with less than 3 words
    data['length'] = data.text.apply(lambda x: len(x.split()) )
    data = data[data['length'] >=3]
    data = data.reset_index().drop(columns=['index', 'length'])

    return data

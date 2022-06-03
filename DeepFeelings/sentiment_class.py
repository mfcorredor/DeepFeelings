import string
import pandas as pd
import re
import numpy as np
import emoji
from amzwbscr_selenium import scrape_amz
from twitter_api import get_lastest_tweets
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForSeq2SeqLM, AutoConfig
import torch

def get_data_sentiment_model(ls_product_id, user_name, n_tweets):
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

def preproc_sentiment_model(ls_product_id, user_name, n_tweets):

    data = get_data_sentiment_model(ls_product_id, user_name, n_tweets)

    # Remove user names
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                                if not word.startswith("@")]))

    #Remove emojis
    data.text = emoji.get_emoji_regexp().sub(u'', df["text"])

    data.text = str(text).lower() #Make text lowercase
    data.text = re.sub('\[.*?\]', '', text) #remove text in square brackets
    data.text = re.sub('https?://\S+|www\.\S+', '', text) #,remove links
    data.text = re.sub('<.*?>+', '', text) #remove punctuation
    data.text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #remove punctuation
    data.text = re.sub('\n', '', text) #containing numbers
    data.text = re.sub('\w*\d\w*', '', text) #remove numbers
    data.text = ''.join([i for i in text if not i.isdigit()]) #remove numbers

    return data

def sentiment_analysis(product_id, user_name, bearer_token, model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"):

    """get the sentiment analysis for a determinated tw user (user_name) and
        its amz products. Arguments: product_id from amz, user_name of tw,
        beaker_token for tw_api"""

    """defines the model and the tokenizer. If a model is not given as argument, roberta will be used by default"""

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    config = AutoConfig.from_pretrained(model_path)

    X_pred = df["text"].tolist()
    prediction = []

    for i in range(1000):
        inputs = self.tokenizer(X_pred[i], return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        prediction.append(self.model.config.id2label[predicted_class_id])

    df["sentiment"] = prediction

    return df

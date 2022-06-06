import pandas as pd
import re
import string
import numpy as np
from sentiment_analysis import get_data_sentiment_model
import emoji
from nltk.corpus import words

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)


def preproc(ls_product_id, user_name, n_tweets=100):

    data = get_data_sentiment_model(ls_product_id, user_name, n_tweets)

    # Remove user names
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                                if not word.startswith("@")]))

    #Remove emojis
    data.text = data.text.apply(lambda x: remove_emoji(x))

    #Make text lowercase
    data.text = data.text.apply(lambda x: x.lower())

    #remove text in square brackets
    data.text = data.text.apply(lambda x: re.sub(r"[ \(\w+\)]", "", x))

    #remove links
    data.text = data.text.apply(lambda x: re.sub('https?://\S+|www\.\S+', '', x))

    #remove some punctuation
    data.text = data.text.apply(lambda x: re.sub('<*>+', '', x))

    #containing numbers
    data.text = data.text.apply(lambda x: re.sub('\n', '', x))

    #remove numbers
    data.text = data.text.apply(lambda x: re.sub('\w*\d\w*', '', x))

    #remove numbers
    #data.text = ''.join([i for i in data.text if not i.isdigit()])

    # Remove user names
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                                if not word.startswith("@")]))

    #Remove non english words
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

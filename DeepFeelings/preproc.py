import pandas as pd
import re
import string
import numpy as np
import emoji
from nltk.corpus import words

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def get_preproc(data):
    """
    Preprocesses the data (texts) to pass to RoBERTa model
        data (DataFrame): df with a text and a date column
    Returns the DataFrame preprocessed
    """

    data["text"] = data["text"].astype(str)

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

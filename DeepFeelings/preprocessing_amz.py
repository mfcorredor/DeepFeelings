import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import re
import numpy as np
import emoji


def remove_emoji(string):
    return emoji.get_emoji_regexp().sub(u'', string)

def clean_text(text):

    text = str(text).lower() #Make text lowercase
    text = re.sub('\[.*?\]', '', text) #remove text in square brackets
    text = re.sub('https?://\S+|www\.\S+', '', text) #,remove links
    text = re.sub('<.*?>+', '', text) #remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #remove punctuation
    text = re.sub('\n', '', text) #containing numbers
    text = re.sub('\w*\d\w*', '', text) #remove numbers
    text = ''.join([i for i in text if not i.isdigit()]) #remove numbers

    return text

def preprocessing(text, list_format = True):
    text = clean_text(text)
    text = remove_emoji(text)
    if list_format:
        text = text.split(" ")
    return text

import pandas as pd
import string
import numpy as np

# Preprocessing
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer

# LDA
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer

def preproc_LDA(data):
    '''Returns a df with the text column preprocessed for LDA model
        data: dataframe with a 'text' column and a 'sentiment' column'''

    # Remove user names
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                                if not word.startswith("@")]))

    # Remove punctuation and lower
    for p in string.punctuation:
        data.text = data.text.str.replace(p, '', regex=True)
    data.text = data.text.str.lower()

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    data.text = data.text.apply(lambda x: ' '.join([word for word in x.split()\
                            if word not in (stop_words)]))

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    data.text = data.text.apply(lambda x: ' '.join([lemmatizer.lemmatize(word)\
                                for word in x.split()]))

    # Remove non english words
    en_words = set(words.words())
    data.text = data.text.apply(lambda x: " ".join(w for w in x.split()\
                                if w in en_words))
    data.text.replace('', np.nan, inplace=True)
    data.dropna(subset=['text'], inplace=True)

    # Remove strings with less than 3 words
    data['length'] = data.text.apply(lambda x: len(x.split()) )
    data = data[data['length'] >=3]
    return data.reset_index().drop(columns=['index', 'length'])

def get_topics_LDA_model(data, n_topics=2):
    '''returns a list of strings with the words for each topic
        data: dataframe with a 'text' column and a 'sentiment' column
        n_topics: number of topics to return'''

    # Preprocess the data, #easier ta
    preproc_LDA(data)

    # Separate positive and negative data to analyse
    data_neg = data[data['sentiment'] == 'Negative']
    data_pos = data[data['sentiment'] == 'Positive']

    # Train the model on negative texts
    vectorizer = TfidfVectorizer().fit(data_neg['text'])
    X = vectorizer.transform(data_neg['text'])
    lda_model = LatentDirichletAllocation(n_components=n_topics).fit(X)

    # Topics for negative texts
    topics_neg = [[vectorizer.get_feature_names()[i]\
            for i in topic.argsort()[:-10 - 1:-1]]\
            for idx, topic in enumerate(lda_model.components_)]
    topics_neg = [' '.join(topic) for topic in topics_neg]

    # Train the model on positive texts
    vectorizer = TfidfVectorizer().fit(data_pos['text'])
    X = vectorizer.transform(data_pos['text'])
    lda_model = LatentDirichletAllocation(n_components=n_topics).fit(X)

    # Topics for positive texts
    topics_pos = [[vectorizer.get_feature_names()[i]\
            for i in topic.argsort()[:-10 - 1:-1]]\
            for idx, topic in enumerate(lda_model.components_)]
    topics_pos = [' '.join(topic) for topic in topics_pos]

    return topics_neg, topics_pos

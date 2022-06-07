
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import string




lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def lemmatize(text_list):
    result = []
    for i in text_list:
        result.append(lemmatizer.lemmatize(i))
    return result

def remove_stop(text_list):
    result = []
    for i in text_list:
        if i in stop_words:
            pass
        elif i == None or "":
            pass
        else:
            result.append(i)
    return result

#remove all punctuation
def remove_punct(text):
    for p in string.punctuation:
        text = text.replace(p, '')
    return text


#preprocess to get most important words in main df column or just as a list
def get_important_words(df, list_output = False):
    df["important_words"] = df["text"].apply(lambda x: x.split(" "))
    df["important_words"] = df["important_words"].apply(lambda x: lemmatize(x))
    df["important_words"] = df["important_words"].apply(lambda x: remove_stop(x))
    df["important_words"] = df["important_words"].apply(lambda x: " ".join(x))
    df["important_words"] = df["important_words"].apply(lambda x: remove_punct(x))

    result = df

    if list_output:
        temp_df = pd.DataFrame()
        temp_df["text"] = df["important_words"]

        list_of_lists_for_each_text = temp_df.values.tolist()
        list_of_strings_for_each_text = []

        for i in list_of_lists_for_each_text:
            list_of_strings_for_each_text.append("".join(i))

        result = list_of_strings_for_each_text

    return result


def get_list_of_strings(df, column_name = "text"):
    temp_df = pd.DataFrame()
    temp_df["text"] = df[column_name]

    list_of_lists_for_each_text = temp_df.values.tolist()
    list_of_strings_for_each_text = []

    for i in list_of_lists_for_each_text:
        list_of_strings_for_each_text.append("".join(i))

    result = list_of_strings_for_each_text

    return result

def get_cloud(df, plotting = False):
    list_of_strings = get_important_words(df, list_output = True)
    string_texts = "".join(list_of_strings)
    if plotting:
        wordcloud = WordCloud().generate(string_texts)
        result = plt.imshow(wordcloud, interpolation='bilinear'), plt.axis("off")
    else:
        result = string_texts
    return result

def get_kmeans_clusters(df, n_clusters = 4, perplexity = 30):
    kmeans = KMeans(n_clusters = n_clusters)
    input_list = get_list_of_strings(df) #preprocessing to list

    #getting the GSE model
    model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(model_url)

    #getting the GSE vectors
    X = model(input_list)
    array = np.array(X)
    vec_df = pd.DataFrame(array)

    #getting the clusters
    y_pred = kmeans.fit_predict(X)
    df["clusters"] = y_pred
    result_df = df

   #reshape to 2dim
    tsne = TSNE(n_components= 2, perplexity= perplexity)
    X_2d = tsne.fit_transform(X)
    X_2d_df = pd.DataFrame(X_2d)

    #final df
    result_df["x"] = X_2d_df[0]
    result_df["y"] = X_2d_df[1]

    return result_df



#the following function works better with the preprocessing from the get_important_words function
#change important_words_input to false if you want to apply to the text column
def get_tf_idf_clusters(df, n_clusters = 4, perplexity = 30, important_words_input = True):
    kmeans = KMeans(n_clusters = n_clusters)


    #creating a list of strings depending on the input column
    if important_words_input:
        list_of_strings = get_list_of_strings(df, column_name = "text")
    else:
        list_of_strings = get_list_of_strings(df, column_name = "important_words")

    bow_df = pd.DataFrame(list_of_strings)
    bow_df.rename(axis = 1, mapper= {0:"text"},inplace=True)

    #Creating word vectors
    tf_idf_vectorizer = TfidfVectorizer()
    X = tf_idf_vectorizer.fit_transform(list_of_strings)
    bow_vec_df = pd.DataFrame(X.toarray(), columns = tf_idf_vectorizer.get_feature_names())

    #KMeans
    y_pred = kmeans.fit_predict(bow_vec_df)
    bow_df["clusters"] = y_pred
    result_df = bow_df

    #reshape to 2dim
    tsne = TSNE(n_components= 2, perplexity= perplexity)
    X_2d = tsne.fit_transform(X)
    X_2d_df = pd.DataFrame(X_2d)

    #final df
    result_df["x"] = X_2d_df[0]
    result_df["y"] = X_2d_df[1]

    return result_df
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

#complex cluster function, do not use this
def get_clusters_plotted(df, default_on_comments =True, default_w_stopwords = True, n_clusters = 4, two_dim_output = True, perplexity = 30, plotting = False):

    kmeans = KMeans(n_clusters = n_clusters)

    if default_on_comments: #GSE on the comments

        #preprocessing to list
        if default_w_stopwords:
            input_list = get_important_words(df, list_output = True)
        else:
             input_list = get_list_of_strings(df)

        #getting the GSE model
        model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        model = hub.load(model_url)

        #getting the GSE vectors
        X = model(input_list)
        array = np.array(X)
        vec_df = pd.DataFrame(array)

        #getting the clusters
        y_pred = kmeans.fit_predict(X)
        df["clusters"] = y_pred
        result_df = df

    else: #tf-idf on all the words
        list_of_strings = get_important_words(df, list_output = True)
        bow = list_of_strings.split(" ")
        #remove duplicates by converting to set and reconverting to list
        #s_bow = set(bow)
        #bow2 = list(s_bow)


        bow_df = pd.DataFrame(bow)
        bow_df.rename(axis = 1, mapper= {0:"text"},inplace=True)

        #W2V
        tf_idf_vectorizer = TfidfVectorizer()
        X = tf_idf_vectorizer.fit_transform(bow)
        bow_vec_df = pd.DataFrame(X.toarray(), columns = tf_idf_vectorizer.get_feature_names())

        #KMeans
        y_pred = kmeans.fit_predict(bow_vec_df)
        bow_df["clusters"] = y_pred
        result_df = bow_df

        result = result_df

    if two_dim_output: #reshape to 2dim
        tsne = TSNE(n_components= 2, perplexity= perplexity)
        X_2d = tsne.fit_transform(X)
        X_2d_df = pd.DataFrame(X_2d)

        #final df
        result_df["x"] = X_2d_df[0]
        result_df["y"] = X_2d_df[1]

        result = result_df

    if plotting:
    #plotting
        fig = px.scatter(
        result_df,
        x="x",
        y="y",
        color="clusters",
        hover_name="text",
        )

        result = fig.show()

    return result

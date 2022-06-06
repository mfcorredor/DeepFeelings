
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

#preprocess to get most important words in main df column or just as a list
def get_important_words(df, list_output = False):
    df["important_words"] = df["texts"].apply(lambda x: x.split(" "))
    df["important_words"] = df["important_words"].apply(lambda x: lemmatize(x))
    df["important_words"] = df["important_words"].apply(lambda x: remove_stop(x))
    df["important_words"] = df["important_words"].apply(lambda x: " ".join(x))

    result = df

    if list_output:
        temp_df = pd.DataFrame()
        temp_df["texts"] = df["important_words"]

        list_of_lists_for_each_text = temp_df.values.tolist()
        list_of_strings_for_each_text = []

        for i in list_of_lists_for_each_text:
            list_of_strings_for_each_text.append("".join(i))

        result = list_of_strings_for_each_text

    return result

# the wordcloud function

def get_list_of_strings(df):
    temp_df = pd.DataFrame()
    temp_df["texts"] = df["texts"]

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


#doing clusters on the single words
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
        s_bow = set(bow)
        bow2 = list(s_bow)

        bow_df = pd.DataFrame(bow2)
        bow_df.rename(axis = 1, mapper= {0:"text"},inplace=True)

        #W2V
        tf_idf_vectorizer = TfidfVectorizer()
        X = tf_idf_vectorizer.fit_transform(bow2)
        bow_vec_df = pd.DataFrame(X.toarray(), columns = tf_idf_vectorizer.get_feature_names())

        #KMeans
        y_pred = kmeans.fit_predict(bow_vec_df)
        bow_df["clusters"] = y_pred
        result_df = bow_df

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
        hover_name="texts",
        )

        result = fig.show()

    return result

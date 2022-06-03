from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
from data import get_data

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

main_df = get_data()
main_df["important_words"] = main_df["texts"].apply(lambda x: x.split(" "))
main_df["important_words"] = main_df["important_words"].apply(lambda x: lemmatize(x))
main_df["important_words"] = main_df["important_words"].apply(lambda x: remove_stop(x))

temp_df = pd.DataFrame()
temp_df["texts"] = main_df["important_words"]
temp_df["texts"] = temp_df["texts"].apply(lambda x: " ".join(x))

list_of_lists_for_each_text = temp_df.values.tolist()
list_of_strings_for_each_text = []


def list_of_strings():
    for i in list_of_lists_for_each_text:
        list_of_strings_for_each_text.append("".join(i))

    return list_of_lists_for_each_text

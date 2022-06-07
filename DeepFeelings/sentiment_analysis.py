from nltk.corpus import words
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForSeq2SeqLM, AutoConfig
import torch

def get_sentiment(data, model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"):

    """get the sentiment analysis for a determinated tw user (user_name) and
        its amz products. Arguments: product_id from amz, user_name of tw,
        beaker_token for tw_api"""

    """defines the model and the tokenizer. If a model is not given as argument, roberta will be used by default"""

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    config = AutoConfig.from_pretrained(model_path)

    #data = preproc(ls_product_id, user_name, n_tweets)
    data["text"] = data["text"].apply(lambda x: " ".join(x.split(" ")[:480]))
    X_pred = data["text"]#.tolist()
    prediction = []

    for i in range(data.shape[0]):
        inputs = tokenizer(X_pred[i], return_tensors="pt")

        with torch.no_grad():
            logits = model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        prediction.append(model.config.id2label[predicted_class_id])

    data["sentiment"] = prediction

    return data

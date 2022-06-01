from DeepFeelings.data import get_data, get_X_pred
from DeepFeelings.preproc import clean_data
from DeepFeelings.results import get_results
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForSeq2SeqLM, AutoConfig
import torch


class Model():
    def __init__(self, model_path):

        """defines the model and the tokenizer as a class attributes"""

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        config = AutoConfig.from_pretrained(model_path)

        self.tokenizer = tokenizer
        self.model = model
        self.config = config

    def prediction(self, X_pred):

        """get the predictions"""
        self.get_model()
        prediction = []

        for i in range(1000):
            inputs = self.tokenizer(X_pred[i], return_tensors="pt")

            with torch.no_grad():
                logits = self.model(**inputs).logits

            predicted_class_id = logits.argmax().item()
            prediction.append(self.model.config.id2label[predicted_class_id])

        return prediction



if __name__ == "__main__":

    # get data
    df = get_data()

    # get X_pred
    X_pred = get_X_pred(df)

    # clean data
    X_pred = clean_data(X_pred)

    # do the sentiment analysis
    model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model_created = Model(model_path)
    prediction = model_created.prediction(X_pred)

    # prepare de data for result platform
    results = get_results(prediction)

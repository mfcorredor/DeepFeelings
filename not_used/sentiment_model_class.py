from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForSeq2SeqLM, AutoConfig
import torch

class Model():
    def __init__(self, model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"):

        """defines the model and the tokenizer as a class attributes"""

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        config = AutoConfig.from_pretrained(model_path)

        self.tokenizer = tokenizer
        self.model = model
        self.config = config

    def prediction(self, df):

        """get the predictions"""
        self.get_model()
        X_pred = df["text"].tolist()
        prediction = []

        for i in range(1000):
            inputs = self.tokenizer(X_pred[i], return_tensors="pt")

            with torch.no_grad():
                logits = self.model(**inputs).logits

            predicted_class_id = logits.argmax().item()
            prediction.append(self.model.config.id2label[predicted_class_id])

        df["sentiment_pred"] = prediction

        return df



if __name__ == "__main__":

    # do the sentiment analysis
    model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model_created = Model(model_path)
    prediction = model_created.prediction(df)

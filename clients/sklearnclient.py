"""Functionality to make predictions from sklearn models"""
import numpy as np
from sklearn.externals import joblib


class SklearnClient:

    def __init__(self, training_file, model_type, model_version, label_list):
        """Constructor

        Args:
            training_file (str): path to training file (contains vectorizer and model)
            model_type (str): type of model
            model_version (str): version of model
            label_list (list of str): List of labels being used
        """

        self.model_type = model_type
        self.model_version = model_version

        self.label_list = label_list
        self.training = joblib.load(training_file)
        self.estimator = self.training['estimator']
        self.vectorizer = self.training['vectorizer']

    def predict(self, text):
        """
        Make a prediction using a trained model for one input utterance

        Args:
            text (string): One utterance to classify
        Returns:
            dict of (prediction (str): predicted class, probabilities (list): probabilities)
        """

        example = self.vectorizer.transform([text])
        probs = self.estimator.predict_proba(example)[0]
        pred = self.label_list[np.argmax(probs)]
        prob_dict = dict(zip(self.label_list, probs))

        return dict(prediction=pred,
                    probabilities=prob_dict,
                    model_type=self.model_type,
                    model_version=self.model_version,
                    tokens='')

import pandas as pd
import numpy as np
from custom_errors import *

class Cosine_sim_classifier:
    def __init__(self, model: pd.DataFrame, labels: str, features: list):
        ## Initialize the classifier with a pre-trained model

        if not isinstance(model, pd.DataFrame):
            raise TypeError("The model must be a pandas DataFrame.")

        if not isinstance(labels, str):
            raise TypeError("The labels must be a string representing the column name of the labels in the model DataFrame.")

        if not isinstance(features, list):
            raise TypeError("The features must be a list of strings representing the column names of the features in the model DataFrame.")

        self.model = model
        self.labels = labels
        self.features = pd.DataFrame(columns = features)

        if self.features.shape[1] != self.model.shape[1] - 1:
            raise InvalidFeaturesError(self.features.shape[1], self.model.shape[1] - 1)

        if self.labels not in self.model.columns or self.labels is None:
            raise InvalidLabelColumnError(self.labels)

    def __init__(self):
        ## Default constructor, loads model from the original disease diagnosis engine           
        self.model = pd.read_csv("./data/output_average.csv")
        self.labels = self.model.columns.tolist()[0]
        self.features = pd.read_csv("./data/features.csv").drop(columns=["Diagnosis", "Age"])

    def similarity(self, vector, k=5):

        if k < 1 or k > self.model.shape[0]:
            raise InvalidTop_KError(k)

        if not isinstance(vector, np.ndarray) or not isinstance(vector, list) or not isinstance(vector, pd.Series) or not (isinstance(vector, pd.DataFrame) and vector.shape[1] == 1):
            raise InvalidVectorTypeError(resulting_type=type(vector))
        
        if len(vector) != self.model.shape[1] - 1:
            raise InvalidVectorSizeError(self.model.shape[1] - 1, len(vector))
        
        vector_len = np.sqrt(vector**2).sum()
        possible_diagnosis = self.model[[self.labels]].copy()
        diagnosis_profiles = self.model.drop(columns = [self.labels])
        scores = []

        for i in range(self.model.shape[0]):
            row = diagnosis_profiles.iloc[i]
            row_len = np.sqrt(row**2).sum()
            dot_product = (row * vector).sum()
            cosine_score = dot_product / (vector_len * row_len)
            scores.append(cosine_score)

        possible_diagnosis["Scores"] = scores
        top_k = possible_diagnosis.sort_values(by="Scores", ascending=False).head(k)
        return top_k

    def get_model(self):
        return self.model

    def get_features(self):
        return self.features

    def get_labels(self):
        return self.labels
    
    def extract_features(self, record: dict):
        if record is None or not isinstance(record, dict):
            raise TypeError("The record must be a dictionary with symptom names as keys and symptom values as values.")

        if len(record) > self.features.shape[1]:
            raise ValueError("The record contains more features than the model supports. Please provide a record with the correct number of features.")
        
        new_record = self.features.copy()
        new_record = new_record.T
        new_record[0] = np.zeros(new_record.shape[0], dtype=int)
        new_record = new_record.T

        given_features = list(record.keys())

        for i in given_features:
            if i not in self.features.columns:
                raise ValueError(f"The symptom '{i}' is not a valid feature. Please provide a record with valid symptom names.")
            new_record[i] = record[i]
        ## Extracts features to be used from a given record structured as a dictionary holding keys and values for each symptom
        ## Expected structure of the dictionary is {symptom_name: symptom_value, ...}. Any not present symptom will be treated as 0 (no information gathered)

        return new_record

    def extract_features(self, record: list):
        if record is None or not isinstance(record, list):
            raise TypeError("The record must be a list of symptom codes.")
        if len(record) > self.features.shape[1]:
            raise ValueError("The record contains more features than the model supports. Please provide a record with the correct number of features.")

        new_record = self.features.copy()
        new_record = new_record.T
        new_record[0] = np.ones(new_record.shape[0], dtype=int) * -1
        new_record = new_record.T

        for i in record:
            if i not in self.features.columns:
                raise ValueError(f"The symptom code '{i}' is not a valid feature. Please provide a record with valid symptom codes.")
            new_record[i] = 1
        ## Extracts features to be used from a given record structured as a list of values for each symptom
        ## Expected structure of the list is [symptom_code_1, symptom_code_2, ...]. Any not present symptom will be treated as -1 (explicitly not present)
        return new_record

    def extract_features(self, record: pd.DataFrame):
        if record is None or not isinstance(record, pd.DataFrame):
            raise TypeError("The record must be a pandas DataFrame with symptom names as columns and symptom values as rows.")
        if record.shape[1] > self.features.shape[1]:
            raise ValueError("The record contains more features than the model supports. Please provide a record with the correct number of features.")

        new_record = self.features.copy()
        new_record = new_record.T
        new_record[0] = np.zeros(new_record.shape[0], dtype=int)
        new_record = new_record.T

        new_record = pd.concat([new_record, record], ignore_index = True)
        if new_record.shape[1] != self.features.shape[1]:
            raise ValueError("The record contains more features than the model supports or the record contains invalid features. Please provide a record with the correct number of features.")
        ## Extracts features to be used from a given record structured as a pandas DataFrame holding columns and rows for each symptom
        ## Expected structure of the DataFrame is columns as symptom names and rows as symptom values. Any not present symptom will be treated as 0 (no information gathered)

        return new_record
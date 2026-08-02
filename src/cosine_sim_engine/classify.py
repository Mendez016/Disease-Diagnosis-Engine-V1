import pandas as pd
import numpy as np
from importlib.resources import files
from .custom_errors import *

class Cosine_sim_classifier:
    def __init__(self, model = None, labels = None):
        if model is None and labels is None:
            self.model = pd.read_csv(files("cosine_sim_engine.data") / "prototype_vectors.csv"  )
            self.labels = self.model.columns.tolist()[0]
            self.features = pd.read_csv(files("cosine_sim_engine.data") / "features.csv").drop(columns=["Diagnosis", "Age"])


        elif model is not None and labels is not None:
            if not isinstance(model, pd.DataFrame):
                raise TypeError("The model must be a pandas DataFrame.")

            if not isinstance(labels, str):
                raise TypeError("The labels must be a string representing the column name of the labels in the model DataFrame.")

            if labels not in model.columns or labels is None:
                raise InvalidLabelColumnError(self.labels)

            self.model = model
            self.labels = labels
            self.features = pd.DataFrame(columns = model.drop(columns=[labels]).columns.to_list())
        else:
            raise ValueError("The model, labels, and features must be provided together or not at all. Please provide all three parameters or none.")

    def similarity(self, vector, k=5):

        if k < 1 or k > self.model.shape[0]:
            raise InvalidTop_KError(k)

        if not isinstance(vector, np.ndarray) and not isinstance(vector, list) and not isinstance(vector, pd.Series) and not isinstance(vector, pd.DataFrame):
            raise InvalidVectorTypeError(resulting_type=type(vector))

        if isinstance(vector, pd.DataFrame):
            vector = vector.iloc[0]
        
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
        return top_k.reset_index(drop=True)

    def get_model(self):
        return self.model

    def get_features(self):
        return self.features

    def get_labels(self):
        return self.labels

    def extract_features(self, data):
        if isinstance(data, dict):
            return self.extract_dict(data)
        elif isinstance(data, list):
            return self.extract_list(data)
        elif isinstance(data, pd.DataFrame):
            return self.extract_df(data)
        else:
            raise TypeError("The record must be a dictionary, list, or pandas DataFrame.")

    def extract_dict(self, record: dict):
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

        return new_record.iloc[[0]]

    def extract_list(self, record: list):
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
        return new_record.iloc[[0]]

    def extract_df(self, record: pd.DataFrame):
        if record.shape[1] > self.features.shape[1]:
            raise ValueError("The record contains more features than the model supports. Please provide a record with the correct number of features.")

        new_record = self.features.copy()

        new_record = pd.concat([new_record, record], ignore_index = True)
        new_record = new_record.fillna(0)
        if new_record.shape[1] != self.features.shape[1]:
            raise ValueError("The record contains more features than the model supports or the record contains invalid features. Please provide a record with the correct number of features.")
        ## Extracts features to be used from a given record structured as a pandas DataFrame holding columns and rows for each symptom
        ## Expected structure of the DataFrame is columns as symptom names and rows as symptom values. Any not present symptom will be treated as 0 (no information gathered)

        return new_record.iloc[[0]]
import pytest
import cosine_sim_engine.custom_errors as ce
from cosine_sim_engine import Cosine_sim_classifier
import pandas as pd
import numpy as np

## Things to test for: Invalid models, invalid number of features on both vectors and on model initialization, invalid label column, invalid top k value, invalid vector type

### Create model exceptions
def test_invalid_arguments():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    with pytest.raises(TypeError):
        Cosine_sim_classifier(model = "not_a_dataframe", labels = "Diagnosis")
    with pytest.raises(TypeError):
        Cosine_sim_classifier(model = df, labels = 123)

def test_incomplete_arguments():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    with pytest.raises(ValueError):
        Cosine_sim_classifier(labels = "Diagnosis")
    with pytest.raises(ValueError):
        Cosine_sim_classifier(model = df)


## Similarity exceptions

def test_invalid_top_k():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    with pytest.raises(ce.InvalidTop_KError):
        my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
        my_model.similarity([1,1], 4)
    with pytest.raises(ce.InvalidTop_KError):
        my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
        my_model.similarity([1,1], 0)

def test_invalid_vector_type():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    with pytest.raises(ce.InvalidVectorTypeError):
        my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
        my_model.similarity("Not a list, np.array, or pd.series", 1)

def test_invalid_vector_size():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    with pytest.raises(ce.InvalidVectorSizeError):
        my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
        my_model.similarity([1,2,3], 1)

## Extraction exceptions

def test_invalid_vector_type_on_extraction():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    with pytest.raises(TypeError):
        my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
        my_model.extract_features("Not a list, dict, or dataframe")

def test_vector_to_extract_longer_than_features():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
    with pytest.raises(ValueError): ## test with a dictionary
        my_model.extract_features({"Feature1": 1, "Feature2": 2, "Feature3": 3})
    with pytest.raises(ValueError): ## test with list
        my_model.extract_features(["Feature1", "Feature2", "Feature3"])
    with pytest.raises(ValueError): ## test with a dataframe
        my_model.extract_features(pd.DataFrame({"Feature1": 1, "Feature2": 2, "Feature3": 3}))

def test_vector_invalid_features():
    df = pd.DataFrame({"Diagnosis": ["Diagnosis1", "Diagnosis2"], "Feature1": [0.1, 0.2], "Feature2": [0.3, 0.4]})
    my_model = Cosine_sim_classifier(model = df, labels = "Diagnosis")
    with pytest.raises(ValueError): ## test with a dictionary
        my_model.extract_features({"Feature1": 1,"Feature3": 3})
    with pytest.raises(ValueError): ## test with list
        my_model.extract_features(["Feature1", "Feature3"])
    with pytest.raises(ValueError): ## test with a dataframe
        my_model.extract_features(pd.DataFrame({"Feature1": 1, "Feature3": 3}))
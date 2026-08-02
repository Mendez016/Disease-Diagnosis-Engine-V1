from cosine_sim_engine import Cosine_sim_classifier
import pandas as pd
import numpy as np
import random

## test extracting from list
def test_extract_list():
    model = Cosine_sim_classifier()
    all_features = model.get_features()
    to_extract = random.sample(all_features.columns.to_list(), 5)
    extracted = model.extract_features(to_extract)
    assert(extracted is not None)
    assert(isinstance(extracted, pd.DataFrame))

def test_extract_dict():
    model = Cosine_sim_classifier()
    all_features = model.get_features()
    to_extract = {}
    sample = random.sample(all_features.columns.to_list(), 5)
    for feature in sample:
        to_extract[feature] = random.choice([-1, 1])
    extracted = model.extract_features(to_extract)
    assert(extracted is not None)
    assert(isinstance(extracted, pd.DataFrame))

def test_extract_df():
    model = Cosine_sim_classifier()
    all_features = model.get_features()
    to_extract = {}
    sample = random.sample(all_features.columns.to_list(), 5)
    for feature in sample:
        to_extract[feature] = random.choice([-1, 1])
    to_extract = pd.DataFrame([to_extract])
    extracted = model.extract_features(to_extract)
    assert(extracted is not None)
    assert(isinstance(extracted, pd.DataFrame))

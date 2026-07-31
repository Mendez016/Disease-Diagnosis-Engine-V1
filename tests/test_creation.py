from cosine_sim_engine import Cosine_sim_classifier
import pandas as pd

def test_load_default():
    classifier = Cosine_sim_classifier()
    assert(classifier is not None)

def test_load_custom():
    model = pd.DataFrame({
        'Diagnosis': ['Disease1', 'Disease2'],
        'Feature1': [0.1, 0.2],
        'Feature2': [0.3, 0.4]
    })
    labels = 'Diagnosis'
    
    classifier = Cosine_sim_classifier(model=model, labels=labels)
    assert(classifier is not None)
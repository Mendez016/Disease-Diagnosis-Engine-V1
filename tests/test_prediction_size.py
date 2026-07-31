from cosine_sim_engine import Cosine_sim_classifier

def test_prediction_size():
    my_model = Cosine_sim_classifier()
    my_vector = my_model.extract_features(["E_91"])
    result  = my_model.similarity(my_vector, 10)
    assert(result.shape[0] == 10)
    
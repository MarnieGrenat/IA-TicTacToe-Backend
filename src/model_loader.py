import json
from deps.model.multilayer_perceptron import MultilayerPerceptron

def load_model(json_path: str) -> MultilayerPerceptron:
    with open(json_path, 'r') as f:
        data = json.load(f)
    return MultilayerPerceptron.from_json(data)

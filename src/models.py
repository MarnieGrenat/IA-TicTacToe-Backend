import joblib
from functools import lru_cache # Evitar problemas de concorrência...

SUPPORTED_MODELS = {
    'mlp' : '../../models/mlp.pkl',
    'dt'  : '../../models/decision_tree.pkl',
    'knn' : '../../models/knn_tictactoe.pkl'
    }

# Cache interno de modelos carregados
_loaded_models = {}

def start_models():
    for model_name, model_path in SUPPORTED_MODELS:
        _loaded_models[model_name] = joblib.load(model_path)

@lru_cache(maxsize=None)
def _get_model(name: str):
    """
    Retorna o modelo já carregado ou faz o load na primeira vez.
    """
    try:
        return _loaded_models[name]
    except:
        raise ValueError(f"Modelo '{name}' não encontrado. Modelos disponíveis: {list(SUPPORTED_MODELS.keys())}")

def predict(model_name, features):
    """
    Faz predição e retorna classe e probabilidades.

    Parâmetros:
    -----------
    model_name : str
        Um dos: 'mlp', 'dt', 'knn'.
    features : list of int/float
        Lista de 9 valores correspondentes às casas do tabuleiro.

    Retorna:
    --------
    tuple:
        (prediction: int, probabilities: List[float])
    """
    model = _get_model(model_name)

    if not isinstance(features, (list, tuple)) or len(features) != 9:
        raise ValueError("Features deve ser list ou tuple com 9 elementos.")

    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0].tolist()
    return int(prediction), [float(p) for p in probability]
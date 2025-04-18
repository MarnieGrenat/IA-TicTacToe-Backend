import joblib
from functools import lru_cache # Evitar problemas de concorrência...

SUPPORTED_MODELS = {
    'mlp' : 'models/mlp.pkl',
    'dt'  : 'models/decision_tree.pkl',
    'knn' : 'models/knn_tictactoe.pkl'
    }

LABEL = {
    0 : "O Victory",
    1 : "Draw",
    2 : "Ongoing",
    3 : "X Victory"
}

# Cache interno de modelos carregados
_loaded_models = {}

@lru_cache(maxsize=None)
def _get_model(name: str):
    if name not in SUPPORTED_MODELS:
        raise ValueError(f"Modelo '{name}' não suportado.")
    return joblib.load(SUPPORTED_MODELS[name])

def predict(model_name : str, features : list[int]):
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

    prediction = int(model.predict([features])[0])
    probability = model.predict_proba([features])[0].tolist()
    return LABEL[prediction], [float(p) for p in probability]

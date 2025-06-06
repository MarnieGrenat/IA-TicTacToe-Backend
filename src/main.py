from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from board.board import Board
from board import resources as bs
from model_loader import load_model
import os

def main(debug=False):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    board = Board()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'model.json')
    mlp_model = load_model(model_path)

    # callback simplesmente chama mlp_model.predict(...)
    def predict(_, features):
        # A MLP escolhe a próxima jogada
        move = mlp_model.predict(features)

        # Converte índice linear (0-8) para coordenadas (x, y)
        x, y = divmod(move, 3)

        # Tenta jogar no tabuleiro com símbolo -1 (O)
        success = board.update_board(-1, x, y)

        # Verifica o resultado do jogo
        if success:
            estado = board.check_wins()
        else:
            estado = -1  # Jogada inválida

        return estado, []

    BoardGet, BoardUpdate, BoardReset, BoardStatus = bs.create_resources(board, predict)

    api.add_resource(BoardGet, '/board/v1/fetch')
    api.add_resource(BoardUpdate, '/board/v1/update')
    api.add_resource(BoardReset, '/board/v1/reset')
    api.add_resource(BoardStatus, '/board/v1/status')

    app.run(debug=debug)

if __name__ == '__main__':
    main(debug=True)

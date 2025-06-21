from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from board.board import Board
from board import resources as bs
from model_loader import load_model
from deps.model import Minimax
import os

def main(debug=False):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    board = Board()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'deps/output/model.json')
    mlp_model = load_model(model_path)

    minimax = Minimax()

    def update_minimax(mode: str):
        try:
            minimax.update(mode)
            return True
        except:
            minimax.update('medium')
            return False

    BoardUpdate, BoardReset, BoardFetch, ChangeMinimax = bs.create_resources(board, mlp_model.predict, minimax.predict, update_minimax)

    api.add_resource(BoardUpdate, '/board/v1/update')
    api.add_resource(BoardReset, '/board/v1/reset')
    api.add_resource(BoardFetch, '/board/v1/fetch')
    api.add_resource(ChangeMinimax, '/minimax/v1/change_mode')

    app.run(debug=debug)

if __name__ == '__main__':
    main(debug=True)

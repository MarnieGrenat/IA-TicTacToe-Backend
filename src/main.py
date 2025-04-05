from flask import Flask
from flask_restful import Api
from board import Board
from board import resources as bs

def main(debug=False):
    app = Flask(__name__)
    api = Api(app)

    board = Board()

    BoardGet, BoardUpdate, BoardReset, BoardStatus = bs.create_resources(board)

    api.add_resource(BoardGet, '/board/v1/fetch')
    api.add_resource(BoardUpdate, '/board/v1/update')
    api.add_resource(BoardReset, '/board/v1/reset')
    api.add_resource(BoardStatus, '/board/v1/status')

    app.run(debug=debug)

if __name__ == '__main__':
    main(debug=True)
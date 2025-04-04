from flask import Flask
from flask_restful import Api
from board.table import Board
import board.resource as bs

def main(debug=False):
    app = Flask(__name__)
    api = Api(app)

    board = Board()

    BoardGet, BoardUpdate, BoardReset, BoardStatus = bs.create_resources(board)

    api.add_resource(BoardGet, '/get')
    api.add_resource(BoardUpdate, '/update')
    api.add_resource(BoardReset, '/reset')
    api.add_resource(BoardStatus, '/get_status')

    app.run(debug=debug)

if __name__ == '__main__':
    main(debug=True)
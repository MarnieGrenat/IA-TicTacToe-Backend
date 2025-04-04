from flask_restful import Resource, reqparse
from board.table import Board

parser = reqparse.RequestParser()
parser.add_argument('data', type=list, location='json', required=False)

def create_resources(board : Board):
    class Reset(Resource):
        def post(self):
            board.reset()
            return {'message' : 'Board reset'}

    class Status(Resource):
        def get(self):
            # Aqui atualizamos a chamada da API da IA
            return {
                    'message' : 'Board class has been collected successfully'}

    class Update(Resource):
        def post(self):
            args    = parser.parse_args()
            s, x, y = args['s'], args['x'], args['y']
            if None in [s, x, y]:
                return {'message' : f'No useful data provided: {s=}, {x=}, {y=}.'}
            board.update_board(s, x, y)

    class Get(Resource):
        def get(self):
            return board.export_board()

    return Get, Update, Reset, Status
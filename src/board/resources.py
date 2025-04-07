from flask_restful import Resource, reqparse
from board import Board

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
            return {'message' : 'Board class has been collected successfully'}

    class Update(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('s', type=int, location='json', required=True)
            parser.add_argument('x', type=int, location='json', required=True)
            parser.add_argument('y', type=int, location='json', required=True)
            args = parser.parse_args()
            s, x, y = args.get('s'), args.get('x'), args.get('y')

            if None in [s, x, y]:
                return {'message' : f'No useful data provided: {s=}, {x=}, {y=}.'}, 400
            if board.update_board(s, x, y):
                return {'message' : 'Board updated successfully',
                        'board': board.export_board()}
            return {'message' : 'Failed to update board'}, 500

    class Get(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('raw', type=bool, location='args', required=False)

            if parser.parse_args().get('raw'):
                return {'message' : 'Presenting raw board', 'board' : board.export_board_raw() }
            return {'message' : 'Presenting board', 'board' : board.export_board() }

    return Get, Update, Reset, Status
from flask_restful import Resource, reqparse
from board import Board

parser = reqparse.RequestParser()
parser.add_argument('data', type=list, location='json', required=False)

def create_resources(board : Board, callback):
    class Reset(Resource):
        def post(self):
            board.reset()
            return {'message' : 'Board reset',
                    'board': board.export_board()
                    }

    class Status(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('model',    type=str,  location='args', required=False, default='dt')
            parser.add_argument('features', type=str, location='args', required=True)
            args = parser.parse_args()

            model_name, features = args.get('model'), args.get('features').split(',')
            features = list(map(int, features))
            try:
                pred, prob = callback(model_name, features)
                return {'prediction' : pred, 'probabilities' : prob}
            except ValueError as e:
                return {'error': str(e)}, 500

    class Update(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('s', type=int, location='json', required=True)
            parser.add_argument('x', type=int, location='json', required=True)
            parser.add_argument('y', type=int, location='json', required=True)
            parser.add_argument('model', type=str, location='json', required=True)
            args = parser.parse_args()
            s, x, y, model = args.get('s'), args.get('x'), args.get('y'), args.get('model')

            if None in [s, x, y]:
                return {'message' : f'No useful data provided: {s=}, {x=}, {y=}.'}, 400
            if board.update_board(s, x, y):
                estado_ia, _ = callback(model, board.flatten_board())
                return {
                    'message': 'Board updated successfully',
                    'board': board.export_board(),
                    'resultado': board.check_wins(),
                    'estado_ia': estado_ia
                }

            return {'message': f'Failed to update board : {s=}, {x=}, {y=}'}, 500

    class Get(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('raw', type=bool, location='args', required=False)

            if parser.parse_args().get('raw'):
                return {'message' : 'Presenting raw board', 'board' : board.export_board_raw() }
            return {'message' : 'Presenting board', 'board' : board.export_board() }

    return Get, Update, Reset, Status

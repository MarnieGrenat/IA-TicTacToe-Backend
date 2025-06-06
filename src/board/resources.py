from flask_restful import Resource, reqparse
from board.board import Board

def create_resources(board: Board, callback):
    class Reset(Resource):
        def post(self):
            board.reset()
            return {
                'message': 'Board reset',
                'board': board.export_board()
            }

    class Status(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('features', type=str, location='args', required=True)
            args = parser.parse_args()
            try:
                features = list(map(int, args['features'].split(',')))
                pred, _ = callback(None, features)
                return {
                    'prediction': pred
                }
            except ValueError as e:
                return {'error': str(e)}, 400

    class Update(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('s', type=int, location='json', required=True)
            parser.add_argument('x', type=int, location='json', required=True)
            parser.add_argument('y', type=int, location='json', required=True)
            args = parser.parse_args()

            s, x, y = args['s'], args['x'], args['y']
            if board.update_board(s, x, y):
                features = board.flatten_board()
                pred, _ = callback(None, features)
                return {
                    'message': 'Board updated successfully',
                    'board': board.export_board(),
                    'resultado': board.check_wins(),
                    'estado_ia': pred
                }
            return {
                'message': f'Failed to update board: {s=}, {x=}, {y=}'
            }, 500

    class Get(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('raw', type=bool, location='args', required=False)
            if parser.parse_args().get('raw'):
                return {
                    'board': board.export_board_raw()
                }
            return {
                'board': board.export_board()
            }

    return Get, Update, Reset, Status

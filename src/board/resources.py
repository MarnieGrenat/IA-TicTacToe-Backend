from flask_restful import Resource, reqparse
from board.board import Board

def create_resources(board: Board, predict):
    class Reset(Resource):
        def post(self):
            board.reset()

            # Let MLP play first
            board.update_board(1, predict(board.board))
            return {
                'message': 'Board reset',
                'board': board.export_board()
            }

    class Update(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('position', type=int, location='json', required=True)
            args = parser.parse_args()

            player_position = args['position']
            player_did_play = board.update_board(-1, player_position)
            if player_did_play:
                # let MLP play
                if board.check_win() == 2: # If ongoing
                    board.update_board(1, predict(board.board))

                return {
                    'message': 'Board updated successfully',
                    'board': board.export_board('3x3'),
                    'resultado': board.check_win()
                }
            return {
                'message': f'Failed to update board: {player_position=}'
            }, 500
    
    class Fetch(Resource):
        def get(self):
            return {
                'board': board.export_board('3x3')
            }


    return Update, Reset, Fetch

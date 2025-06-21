from flask_restful import Resource, reqparse
from board.board import Board
from deps.model import MultilayerPerceptron, Minimax


def create_resources(board: Board, predict_mlp, predict_minimax):
    class Reset(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('modo', type=str, location='json', default='mlp')
            args = parser.parse_args()
            modo = args['modo']

            board.reset()

            # IA joga primeiro apenas nos modos "mlp" ou "minimax"
            if modo in ['mlp', 'minimax']:
                ia_symbol = 1  # X
                prediction = predict_mlp(board.board) if modo == 'mlp' else predict_minimax(board.board)
                board.update_board(ia_symbol, prediction)

            return {
                'message': 'Board reset',
                'board': board.export_board('3x3')
            }

    class Update(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('position', type=int, location='json', required=False)
            parser.add_argument('modo', type=str, location='json', default='mlp')
            args = parser.parse_args()

            modo = args['modo']
            pos = args['position']

            if modo == 'treino':
                # Turno automático entre MLP e Minimax até terminar
                current_player = 1 if board.board.count(0) % 2 == 1 else -1
                predict_func = predict_mlp if current_player == 1 else predict_minimax

                prediction = predict_func(board.board)
                board.update_board(current_player, prediction)

                return {
                    'message': 'Treinamento automático',
                    'board': board.export_board('3x3'),
                    'resultado': board.check_win(),
                    'estado_ia': predict_mlp(board.board)  # previsão da IA mesmo no modo treino
                }

            # Jogador humano fez uma jogada (como O)
            success = board.update_board(-1, pos)
            if not success:
                return {'message': 'Jogada inválida', 'position': pos}, 400

            # Verifica se o jogo continua
            if board.check_win() == 2:
                # IA responde (MLP ou Minimax)
                ia_prediction = predict_mlp(board.board) if modo == 'mlp' else predict_minimax(board.board)
                board.update_board(1, ia_prediction)

            return {
                'message': 'Board atualizado',
                'board': board.export_board('3x3'),
                'resultado': board.check_win(),
                'estado_ia': predict_mlp(board.board)
            }

    class Fetch(Resource):
        def get(self):
            return {
                'board': board.export_board('3x3')
            }

    return Update, Reset, Fetch

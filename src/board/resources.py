from flask_restful import Resource, reqparse
from board.board import Board
from deps.model import MultilayerPerceptron, Minimax


def create_resources(board: Board, predict_mlp, predict_minimax, update_minimax):
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
                # valida jogada da IA
                if not board.update_board(ia_symbol, prediction):
                    return {'message': 'Jogada inválida da IA', 'position': prediction}, 400

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
            pos = args.get('position')

            # modo de treino: IA alternando até fim
            if modo == 'treino':
                current_player = 1 if board.board.count(0) % 2 == 1 else -1
                predict_func = predict_mlp if current_player == 1 else predict_minimax
                prediction = predict_func(board.board)
                if not board.update_board(current_player, prediction):
                    return {'message': 'Jogada inválida no treino', 'position': prediction}, 400
                return {
                    'message': 'Treinamento automático',
                    'board': board.export_board('3x3'),
                    'resultado': board.check_win(),
                    'estado_ia': prediction
                }

            # jogada humana (O)
            if pos is None or not board.update_board(-1, pos):
                return {'message': 'Jogada inválida', 'position': pos}, 400

            # turno da IA
            if board.check_win() == 2:
                ia_prediction = predict_mlp(board.board) if modo == 'mlp' else predict_minimax(board.board)
                if not board.update_board(1, ia_prediction):
                    return {'message': 'Jogada inválida da IA', 'position': ia_prediction}, 400

            return {
                'message': 'Board atualizado',
                'board': board.export_board('3x3'),
                'resultado': board.check_win(),
                'estado_ia': ia_prediction if modo != 'treino' else predict_mlp(board.board)
            }

    class Fetch(Resource):
        def get(self):
            return {'board': board.export_board('3x3')}

    class ChangeMode(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('modo', type=str, location='json', default='medium')
            args = parser.parse_args()
            mode = args['modo']
            ok = update_minimax(mode)
            return {
                'message': 'Minimax atualizado' if ok else 'Falha ao atualizar',
                'mode': mode
            }, (200 if ok else 400)

    return Update, Reset, Fetch, ChangeMode

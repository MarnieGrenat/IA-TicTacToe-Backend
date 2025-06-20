class Board:
    """
    Versão do tabuleiro 1x9 em matriz linearizada.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.board =   [0, 0, 0,
                        0, 0, 0,
                        0, 0, 0]

    def update_board(self, symbol: int, pos: int) -> bool:
        """
        Atualiza o tabuleiro com a jogada (x,y).

        Parâmetros:
        -----------
        symbol : int  → +1 (X) ou –1 (O)
        pos    : int  → posição [0..8]

        Retorna:
        --------
        True se célula estava vazia e símbolo válido,
        caso contrário False.
        """
        if self._valid_coordinates(pos) and self._valid_symbol(symbol) and self.board[pos] == 0:
            self.board[pos] = symbol
            return True
        return False

    def export_board(self, format : str='1x9'):
        """
        Retorna uma versão “bonita” do tabuleiro, substituindo
        -1→'O', +1→'X', 0→''.
        """
        result_1x9 = ['', '', '', '', '', '', '', '', '']
        result_3x3 = [['', '', ''], ['', '', ''], ['', '', '']]
        for pos in range(len(self.board)):
            if self.board[pos] == 1:
                result_1x9[pos] = 'X'
            elif self.board[pos] == -1:
                result_1x9[pos] = 'O'

        for i in range(len(self.board)):
            result_3x3[i%3][i//3] = result_1x9[i]
        if format == '1x9':
            return result_1x9
        elif format == '3x3':
            return result_3x3
        else:
            raise ValueError(f'Invalid Input={format}')

    @staticmethod
    def to_int(b: list[str]) -> list[int]:
        result = [0,0,0,0,0,0,0,0,0]
        for i in range(len(b)):
            match b[i]:
                case '' : result[i] = 0
                case 'X': result[i] = 1
                case 'O': result[i] = -1
        return result

    def check_win(self) -> int:
        """
        Verifica o estado atual do tabuleiro (representado como lista linear 1x9).

        Retorna:
        --------
        int : Código do estado do jogo.
            0  : Empate
            1  : X venceu
            2  : Jogo em andamento
            3  : O venceu
        """
        b = self.board

        for i in [0, 3, 6]:
            if b[i] == b[i + 1] == b[i + 2] != 0:
                return self._getlabel(b[i])
        for i in [0, 1, 2]:
            if b[i] == b[i + 3] == b[i + 6] != 0:
                return self._getlabel(b[i])

        # Verifica diagonais
        if (b[0] == b[4] == b[8] != 0) or (b[2] == b[4] == b[6] != 0):
            return b[4]

        if 0 in b:
            return 2 # Em progesso
        return 0 # Empate

    def _valid_coordinates(self, pos: int) -> bool:
        """
        Verifica se as coordenadas (x,y) estão dentro do tabuleiro 3x3 (0..2).
        """
        return 0 <= pos  <= 8

    def _valid_symbol(self, symbol: int) -> bool:
        """
        Verifica se o símbolo é válido (-1 ou +1).
        """
        return symbol in [-1, 1]

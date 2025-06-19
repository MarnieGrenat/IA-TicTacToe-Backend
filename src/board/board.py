from .utils import valid_coordinates, valid_symbol

class Board:
    """
    Versão do tabuleiro 3x3 em matriz (não linearizada).
    """

    def __init__(self):
        self.board = self.clear()

    def clear(self):
        return [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]

    def reset(self):
        self.board = self.clear()

    def update_board(self, symbol: int, x: int, y: int) -> bool:
        """
        Atualiza o tabuleiro com a jogada (x,y).

        Parâmetros:
        -----------
        symbol : int  → +1 (X) ou –1 (O)
        x, y   : int  → coordenadas [0..2]

        Retorna:
        --------
        True se célula estava vazia e símbolo válido, 
        caso contrário False.
        """
        if valid_coordinates(x, y) and valid_symbol(symbol) and self.board[x][y] == 0:
            self.board[x][y] = symbol
            return True
        return False

    def flatten_board(self):
        """
        Converte a matriz 3×3 em lista de 9 elementos (linha‐a‐linha).
        """
        return [cell for row in self.board for cell in row]

    def export_board(self):
        """
        Retorna uma versão “bonita” do tabuleiro, substituindo
        -1→'O', +1→'X', 0→''.
        """
        result = [['', '', ''], ['', '', ''], ['', '', '']]
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:
                    result[i][j] = 'X'
                elif self.board[i][j] == -1:
                    result[i][j] = 'O'
        return result

    def export_board_raw(self):
        """
        Retorna o estado bruto (lista de listas de inteiros).
        """
        return self.board

    def check_wins(self):
        """
        Verifica se alguém ganhou, empatou ou ainda há jogadas possíveis.

        Retorna:
        --------
        3 → X venceu
        0 → O venceu
        1 → Empate
        2 → Jogo em andamento
        """
        b = self.board
        # Diagonais
        if b[0][0] == b[1][1] == b[2][2] != 0:
            return 0 if b[1][1] == -1 else 3
        if b[0][2] == b[1][1] == b[2][0] != 0:
            return 0 if b[1][1] == -1 else 3
        # Linhas/colunas
        for i in range(3):
            if b[0][i] == b[1][i] == b[2][i] != 0:
                return 0 if b[0][i] == -1 else 3
            if b[i][0] == b[i][1] == b[i][2] != 0:
                return 0 if b[i][0] == -1 else 3
        # Em andamento ou empate
        if any(cell == 0 for row in b for cell in row):
            return 2
        return 1

from board.utils import *

class Board:
    def __init__(self):
        self.board = self.clear()

    def clear(self):
        return [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]

    def reset(self):
        self.board = self.clear()

    def update_board(self, symbol: int, x: int, y: int) -> bool:
        '''update board status. | symbol= int (-1 or 1) | x= coordinate x between 0 and 2 | y= coordinate y between 0 and 2'''
        if (self.board[x][y] != '0') and valid_coordinates(x, y) and valid_symbol(symbol):
            self.board[x][y] = symbol
            return True
        return False

    def export_board(self) -> list[list[str]]:
        '''Export board containing visual symbols (prettify)'''
        result = [['', '', ''],
                  ['', '', ''],
                  ['', '', '']]

        for x in range(len(result)):
            for y in range(len(result)):
                match self.board[x][y]:
                    case -1 : result[x][y] = 'O'
                    case  1 : result[x][y] = 'X'
        return result

    def export_board_raw(self):
        return self.board
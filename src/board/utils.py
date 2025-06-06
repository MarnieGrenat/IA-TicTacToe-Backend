def valid_coordinates(x: int, y: int) -> bool:
    """
    Verifica se as coordenadas (x,y) estão dentro do tabuleiro 3x3 (0..2).
    """
    return 0 <= x < 3 and 0 <= y < 3

def valid_symbol(symbol: int) -> bool:
    """
    Verifica se o símbolo é válido (-1 ou +1).
    """
    return symbol in [-1, 1]

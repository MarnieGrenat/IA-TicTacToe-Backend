def valid_coordinates(x : int, y : int) -> bool:
    return (x < 3) and (x >= 0) and (y < 3) and (y >= 0)

def valid_symbol(symbol : str) -> bool:
    return symbol in [-1, 1]
import pathlib

from code_c.sudoku.board import board_01, board_02
from code_c.sudoku.helper import SudokuParser, extract_board_from_image


def test_solve_sudoku():
    sp = SudokuParser(board_02)
    print()
    sp.solve()
    sp.print_board()


def test_extract_board_from_image():
    images = pathlib.Path("../Snipaste_2025-07-17_12-58-36.png")
    rr = extract_board_from_image(str(images))
    print()
    print(rr)
    sp = SudokuParser(rr)
    sp.solve()
    sp.print_board()



import cv2
import pytesseract
import numpy as np


def reorder_points(pts: np.ndarray) -> np.ndarray:
    """將輪廓的四個點重新排序成 [左上, 右上, 右下, 左下]"""
    pts = pts.reshape((4, 2))
    new_pts = np.zeros((4, 2), dtype=np.float32)

    s = pts.sum(axis=1)
    new_pts[0] = pts[np.argmin(s)]  # 左上
    new_pts[2] = pts[np.argmax(s)]  # 右下

    diff = np.diff(pts, axis=1)
    new_pts[1] = pts[np.argmin(diff)]  # 右上
    new_pts[3] = pts[np.argmax(diff)]  # 左下

    return new_pts


def warp_to_square(image: np.ndarray, contour: np.ndarray, size: int = 450) -> np.ndarray:
    """將盤面區塊轉換成正方形視角"""
    # 逼近為四邊形（只保留四點）
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

    if len(approx) != 4:
        raise ValueError("輪廓點數不是 4，無法進行透視轉換")

    pts = reorder_points(approx)

    dst = np.array([
        [0, 0],
        [size - 1, 0],
        [size - 1, size - 1],
        [0, size - 1]
    ], dtype=np.float32)

    # 產生轉換矩陣
    M = cv2.getPerspectiveTransform(pts, dst)

    # 執行透視轉換
    warped = cv2.warpPerspective(image, M, (size, size))

    return warped

def preprocess_cell(cell_img: np.ndarray) -> np.ndarray:
    # 裁切邊緣（防止邊框干擾）
    margin = 4
    h, w = cell_img.shape[:2]
    cell = cell_img[margin:h - margin, margin:w - margin]

    # 放大影像（tesseract 對小圖辨識很差）
    cell = cv2.resize(cell, (100, 100), interpolation=cv2.INTER_LINEAR)

    # 轉灰階
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY) if len(cell.shape) == 3 else cell

    # 自適應閾值二值化（提升文字對比）
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # 去除小雜訊（如邊框點或陰影）
    kernel = np.ones((3, 3), np.uint8)
    denoised = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    return denoised

def extract_board_from_image(image_path: str) -> list[list[int]]:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    # 找出最大正方形（可能是盤面）
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = max(contours, key=cv2.contourArea)

    # 透視轉換（warp）讓盤面變成正的
    # => 省略細節，可以另外補
    warped = warp_to_square(gray, largest)  # 你需要寫 warp_to_square()

    # 切割成 9x9 小格
    cell_height = warped.shape[0] // 9
    cell_width = warped.shape[1] // 9
    board = []

    for i in range(9):
        row = []
        for j in range(9):
            x = j * cell_width
            y = i * cell_height
            cell_img = warped[y:y + cell_height, x:x + cell_width]
            cell_text = pytesseract.image_to_string(cell_img, config='--psm 10 digits')
            digit = int(cell_text.strip()) if cell_text.strip().isdigit() else 0
            row.append(digit)
        board.append(row)

    return board


class SudokuParser:
    def __init__(self, board: list[list[int]]):
        self.is_valid_board(board)
        self.board = board

    def is_valid_board(self, board: list[list[int]]):
        if len(board) != 9:
            raise ValueError('Row is not 9 row')
        if not all(isinstance(row, list) for row in board):
            raise ValueError('Board is not nested')
        for row in board:
            if len(row) != 9:
                raise ValueError('Cell is not 9 cell')
            if not all(isinstance(cell, int) for cell in row):
                raise ValueError('Cell must be an integer')
            if not all(0 <= cell <= 9 for cell in row):
                raise ValueError('Cell must be between 0 and 9')

    def print_board(self):
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j, val in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(val if val != 0 else ".", end=" ")
            print()

    def find_empty(self) -> tuple[int, int] | None:
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def valid(self, num: int, pos: tuple[int, int]):
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self) -> bool:
        find = self.find_empty()
        if find is None:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0
        return False

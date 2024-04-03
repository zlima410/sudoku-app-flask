from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def is_safe(num, grid, row, col):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def fill_diagonal_boxes(grid):
    for i in range(0, 9, 3):
        fill_box(grid, i, i)

def fill_box(grid, row, col):
    for i in range(3):
        for j in range(3):
            num = random.randint(1, 9)
            while not is_safe(num, grid, row + i, col + j):
                num = random.randint(1, 9)
            grid[row + i][col + j] = num

def solve_sudoku(grid):
    empty = find_empty_location(grid)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_safe(num, grid, row, col):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def remove_numbers_from_grid(grid, cells_to_remain):
    count = 81 - cells_to_remain  # Calculate the number of cells to clear
    while count > 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if grid[i][j] != 0:
            grid[i][j] = 0
            count -= 1

@app.route('/new_puzzle', methods=['GET'])
def new_puzzle():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_diagonal_boxes(grid)
    solve_sudoku(grid)
    remove_numbers_from_grid(grid, random.randint(27, 36))  # Ensure 27 to 36 cells remain filled
    return jsonify(grid)

@app.route('/solve_puzzle', methods=['POST'])
def solve_puzzle():
    # Parse the incoming JSON data (the Sudoku grid)
    data = request.get_json()

    # The incoming data should be a 9x9 grid, but validate as needed
    grid = data.get('grid')
    if not grid or len(grid) != 9 or any(len(row) != 9 for row in grid):
        return jsonify({"error": "Invalid grid"}), 400

    # Attempt to solve the Sudoku puzzle
    if solve_sudoku(grid):
        return jsonify(grid)  # Return the solved grid
    else:
        return jsonify({"error": "Could not solve the puzzle"}), 500

if __name__ == '__main__':
    app.run(debug=True)

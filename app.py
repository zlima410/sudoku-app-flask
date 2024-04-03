from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def is_valid(grid, row, col, num):
    # Check if num is not in the given row
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # Check if num is not in the given column
    for x in range(9):
        if grid[x][col] == num:
            return False
    
    # Check if num is not in the 3x3 matrix
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(grid):
    empty = find_empty_location(grid)
    if not empty:
        return True
    else:
        row, col = empty
    
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
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

def remove_numbers_from_grid(grid, num_remove):
    count = num_remove
    while count > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            count -= 1
    return grid

@app.route('/generate', methods=['GET'])
def generate_sudoku():
    grid = [[0 for x in range(9)] for y in range(9)]
    
    # Attempt to fill the grid with a solved puzzle
    if solve_sudoku(grid):
        # Successfully solved, now remove numbers to create a puzzle
        puzzle = remove_numbers_from_grid(grid, 40)  # Remove 40 numbers as an example
    else:
        puzzle = grid  # Fallback, should not happen in this context
    
    puzzle_formatted = [''.join(str(num) for num in row) for row in puzzle]
    puzzle_str = '\n'.join(puzzle_formatted)
    
    return jsonify({
        'id': 1,
        'puzzle': puzzle_str
    })

# Route for getting a specific puzzle by ID
@app.route('/get/<int:puzzle_id>', methods=['GET'])
def get_puzzle(puzzle_id):
    # Logic to retrieve a puzzle by its ID
    puzzle = {
        'id': puzzle_id,
        'puzzle': ''
    }
    return jsonify(puzzle)

# Route for solving a Sudoku puzzle
@app.route('/solve', methods=['POST'])
def solve_sudoku():
    # Sudoku solving logic goes here
    # Extract puzzle from the request for solving
    request_data = request.get_json()
    puzzle = request_data['puzzle']
    # Here, you'd solve the puzzle
    solution = 'solved puzzle data'
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sudoku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle = db.Column(db.String(81), nullable=False)
    solution = db.Column(db.String(81), nullable=True)

@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    db.create_all()
    print("Initialized the database.")

def generate_random_puzzle():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side
    
    def shuffle(s):
        return random.sample(s, len(s))
    
    row_base = range(base)
    rows = [g * base + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * base + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, base * base + 1))

    # create board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 4
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

@app.route('/generate', methods=['GET'])
def generate_puzzle():
    puzzle = generate_random_puzzle()

    # Convert the puzzle to a string for easy display or storage
    puzzle_str = ''.join([''.join(str(num) for num in row) for row in puzzle])

    # Create a new Sudoku instance with the generated puzzle
    new_puzzle = Sudoku(puzzle=puzzle_str, solution=None)  # Assuming solution is not generated at this point

    # Save the puzzle to the database
    db.session.add(new_puzzle)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Puzzle generated successfully',
        'puzzle': puzzle_str,
        'id': new_puzzle.id  # Return the ID of the newly created puzzle
    })

@app.route('/get', methods=['GET'])
def get_last_puzzle():
    # Query the database for the last puzzle based on the highest ID
    last_puzzle = Sudoku.query.order_by(Sudoku.id.desc()).first()
    
    # Check if a puzzle was found
    if last_puzzle:
        return jsonify({
            'status': 'success',
            'message': 'Last puzzle retrieved successfully',
            'id': last_puzzle.id,
            'puzzle': last_puzzle.puzzle,
            'solution': last_puzzle.solution  # Include this if you want to return the solution as well
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No puzzles found'
        }), 404
    
def solve_sudoku(puzzle):
    puzzle_list = [list(map(int, puzzle[i:i+9])) for i in range(0, 81, 9)]  # Convert string to list of lists
    
    def is_valid(num, pos, bo):
        # Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if bo[i][j] == num and (i,j) != pos:
                    return False

        return True

    def solve(bo):
        find = find_empty(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if is_valid(i, (row, col), bo):
                bo[row][col] = i

                if solve(bo):
                    return True

                bo[row][col] = 0

        return False

    def find_empty(bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i, j)  # row, col

    solve(puzzle_list)
    return ''.join([''.join(str(num) for num in row) for row in puzzle_list])  # Convert list of lists back to string

@app.route('/solve', methods=['GET'])
def solve_last_puzzle():
    # Get the last puzzle generated
    last_puzzle = Sudoku.query.order_by(Sudoku.id.desc()).first()

    if last_puzzle:
        # Solve the puzzle
        solution = solve_sudoku(last_puzzle.puzzle)

        # Update the solution in the database
        last_puzzle.solution = solution
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Puzzle solved successfully',
            'id': last_puzzle.id,
            'solution': solution
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No puzzles found'
        }), 404

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)

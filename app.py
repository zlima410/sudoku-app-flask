from flask import Flask, jsonify
import random

app = Flask(__name__)

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

    # In a real app, you might save the puzzle to a database here
    # For demonstration purposes, we'll skip database operations

    return jsonify({
        'status': 'success',
        'message': 'Puzzle generated successfully',
        'puzzle': puzzle_str,
        # If saving to a database, you would retrieve an ID
        # 'id': puzzle_id 
    })

if __name__ == '__main__':
    app.run(debug=True)

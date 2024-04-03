import React, { useState } from "react";
import axios from "axios";

const SudokuBoard = () => {
  const [board, setBoard] = useState(
    Array(9)
      .fill()
      .map(() => Array(9).fill(""))
  );

  const fetchNewPuzzle = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/new_puzzle");
      setBoard(response.data);
    } catch (error) {
      console.error("Error fetching new puzzle:", error);
    }
  };

  const solveSudoku = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/solve_puzzle", board);
      setBoard(response.data);
    } catch (error) {
      console.error("Error solving puzzle:", error);
    }
  };

  const handleChange = (row, col, value) => {
    const newBoard = [...board];
    newBoard[row][col] = value;
    setBoard(newBoard);
  };

  return (
    <div>
      <button onClick={fetchNewPuzzle}>New Puzzle</button>
      <button onClick={solveSudoku}>Solve Sudoku</button> {/* Solve Sudoku Button */}
      <div className="sudoku-board">
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <input
                key={`${rowIndex}-${colIndex}`}
                type="text"
                maxLength="1"
                value={cell}
                onChange={(e) => handleChange(rowIndex, colIndex, e.target.value)}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SudokuBoard;

import React, { useState } from "react";
import axios from "axios"; // Import Axios

const SudokuBoard = () => {
  const [board, setBoard] = useState(
    Array(9)
      .fill()
      .map(() => Array(9).fill(""))
  );

  // Function to fetch a new puzzle from the Flask backend
  const fetchNewPuzzle = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/new_puzzle");
      setBoard(response.data);
    } catch (error) {
      console.error("Error fetching new puzzle:", error);
    }
  };

  const handleChange = (row, col, value) => {
    const newBoard = [...board];
    newBoard[row][col] = value;
    setBoard(newBoard);
  };

  return (
    <div>
      <button onClick={fetchNewPuzzle}>New Puzzle</button> {/* New Puzzle Button */}
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

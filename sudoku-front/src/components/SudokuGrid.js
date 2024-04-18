import React from "react";
import Cell from "./Cell";

function SudokuGrid({ puzzle, setPuzzle }) {
  const updatePuzzle = (newValue, row, col) => {
    const newPuzzle = puzzle.map((r, i) => r.map((c, j) => (i === row && j === col ? newValue : c)));
    setPuzzle(newPuzzle);
  };

  return (
    <div className="grid">
      {puzzle.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <Cell
            key={`${rowIndex}-${colIndex}`}
            initialValue={cell}
            updatePuzzle={updatePuzzle}
            rowIndex={rowIndex}
            colIndex={colIndex}
          />
        ))
      )}
    </div>
  );
}

export default SudokuGrid;

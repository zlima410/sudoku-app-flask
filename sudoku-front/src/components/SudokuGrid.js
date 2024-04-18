import React from 'react';
import Cell from './Cell';

function SudokuGrid({ puzzle, setPuzzle }) {
  const handleChange = (value, row, col) => {
    const newPuzzle = puzzle.map((r, i) =>
      i === row ? r.map((c, j) => j === col ? value : c) : r
    );
    setPuzzle(newPuzzle);
  };

  return (
    <div className="grid">
      {puzzle.map((row, rowIndex) =>
        row.map((value, colIndex) => (
          <Cell
            key={`${rowIndex}-${colIndex}`}
            value={value}
            onChange={(value) => handleChange(value, rowIndex, colIndex)}
            isBlockBorder={(rowIndex % 3 === 2) && (rowIndex !== 8) && (colIndex % 3 === 2) && (colIndex !== 8)}
          />
        ))
      )}
    </div>
  );
}

export default SudokuGrid;


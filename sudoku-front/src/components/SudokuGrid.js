import React from 'react';
import Cell from './Cell';

function SudokuGrid({ puzzle, setPuzzle }) {
    const updatePuzzle = (newValue, row, col) => {
        const newPuzzle = [...puzzle];
        newPuzzle[row][col] = newValue;  // Update confirmed value
        setPuzzle(newPuzzle);
    };

    return (
        <div className="grid">
            {puzzle.map((row, rowIndex) =>
                row.map((value, colIndex) => (
                    <Cell
                        key={`${rowIndex}-${colIndex}`}
                        initialValue={value}
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



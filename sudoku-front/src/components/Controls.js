import React from 'react';

function Controls({ onSolve, onReset }) {
  return (
    <div>
      <button onClick={onSolve}>Solve Puzzle</button>
      <button onClick={onReset}>New Puzzle</button>
    </div>
  );
}

export default Controls;


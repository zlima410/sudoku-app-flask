import React, { useState, useEffect } from 'react';
import SudokuGrid from './components/SudokuGrid';
import Controls from './components/Controls';
import './App.css';

function App() {
  const [puzzle, setPuzzle] = useState([]);
  const [solution, setSolution] = useState([]);

  useEffect(() => {
    fetchNewPuzzle();
  }, []);

  const fetchNewPuzzle = () => {
    fetch('http://localhost:5000/new_puzzle')
      .then(response => response.json())
      .then(data => {
        setPuzzle(data.grid);
        setSolution(data.grid.map(row => [...row]));
      })
      .catch(error => console.error('Error fetching new puzzle:', error));
  };

  const handleReset = () => {
    fetchNewPuzzle();
  };

  const handleSolve = () => {
    fetch('http://localhost:5000/solve_puzzle', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ grid: solution }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        setSolution(data.grid);
      }
    })
    .catch(error => console.error('Error solving puzzle:', error));
  };

  return (
    <div className="App">
      <h1>Sudoku Game</h1>
      <SudokuGrid puzzle={solution} setPuzzle={setSolution} />
      <Controls onSolve={handleSolve} onReset={handleReset} />
    </div>
  );
}

export default App;

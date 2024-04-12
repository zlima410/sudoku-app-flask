import React from "react";
import "./App.css";
import SudokuBoard from "./components/SudokuBoard";

function App() {
  return (
    <div className="App">
      <h1>Sudoku Solver</h1>
      <SudokuBoard />
    </div>
  );
}

export default App;

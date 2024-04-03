import React, { useState } from "react";
import axios from "axios";

function SudokuGenerator() {
  const [puzzle, setPuzzle] = useState("");

  const generatePuzzle = () => {
    axios
      .get("http://localhost:5000/generate")
      .then((response) => {
        console.log("Puzzle generated. ID:", response.data.id);
        setPuzzle(response.data.puzzle); // Set the puzzle state
      })
      .catch((error) => console.error("There was an error!", error));
  };

  const getPuzzle = () => {
    axios
      .get("http://localhost:5000/get")
      .then((response) => {
        setPuzzle(response.data.puzzle);
      })
      .catch((error) => console.error("There was an error fetching the puzzle!", error));
  };

  const puzzleToGrid = (puzzleString) => {
    let grid = [];
    for (let i = 0; i < puzzleString.length; i += 9) {
      let row = puzzleString.slice(i, i + 9).split("");
      grid.push(row);
    }
    return grid;
  };

  const renderPuzzle = () => {
    let grid = puzzleToGrid(puzzle);
    return grid.map((row, rowIndex) => (
      <div key={rowIndex} style={{ display: "flex" }}>
        {row.map((cell, cellIndex) => (
          <div
            key={cellIndex}
            style={{
              width: "20px",
              height: "20px",
              border: "1px solid black",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            {cell !== "0" ? cell : ""}
          </div>
        ))}
      </div>
    ));
  };

  return (
    <div>
      <button onClick={generatePuzzle}>Generate Puzzle</button>
      <button onClick={getPuzzle}>Get Last Puzzle</button>
      <div style={{ display: "inline-block", marginTop: "20px" }}>{renderPuzzle()}</div>
    </div>
  );
}

export default SudokuGenerator;

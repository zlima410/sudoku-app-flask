import React, { useState } from "react";
import axios from "axios";

function SudokuGenerator() {
  const [puzzle, setPuzzle] = useState("");

  const generatePuzzle = () => {
    axios
      .get("http://localhost:5000/generate")
      .then((response) => {
        // Assuming the puzzle string is directly usable in your front end
        setPuzzle(response.data.puzzle);
      })
      .catch((error) => console.error("There was an error!", error));
  };

  return (
    <div>
      <button onClick={generatePuzzle}>Generate Puzzle</button>
      <p>{puzzle}</p>
    </div>
  );
}

export default SudokuGenerator;

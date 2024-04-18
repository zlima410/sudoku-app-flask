import React, { useState } from "react";

function Cell({ initialValue, updatePuzzle, rowIndex, colIndex }) {
  const [value, setValue] = useState(initialValue); // Confirmed values
  const [sketch, setSketch] = useState(""); // Sketch values
  const [mode, setMode] = useState("input"); // Mode: 'input' or 'sketch'

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      switchMode(); // Switch mode on Enter key press
      e.preventDefault();
      return;
    }

    if (mode === "input" && "123456789".includes(e.key)) {
      setValue(e.key);
      updatePuzzle(e.key, rowIndex, colIndex);
    } else if (mode === "sketch" && "123456789".includes(e.key)) {
      const newSketch = sketch.length < 9 ? sketch + e.key : sketch;
      setSketch(newSketch);
    }
    e.preventDefault(); // Prevent default to manage input manually
  };

  const switchMode = () => {
    setMode(mode === "input" ? "sketch" : "input");
  };

  const clearSketch = () => {
    if (mode === "sketch") setSketch("");
  };

  return (
    <div className={`cell ${mode}`} onClick={clearSketch} onDoubleClick={switchMode}>
      <span className="value">{value}</span>
      <span className="sketch">{sketch}</span>
      <input type="text" onKeyDown={handleKeyPress} />
    </div>
  );
}

export default Cell;

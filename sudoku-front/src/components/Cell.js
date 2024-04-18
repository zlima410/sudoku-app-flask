import React, { useState } from 'react';

function Cell({ initialValue, updatePuzzle, rowIndex, colIndex }) {
    const [value, setValue] = useState(initialValue);
    const [sketch, setSketch] = useState('');
    const [mode, setMode] = useState('input');  // Modes: 'input', 'sketch'

    const handleKeyPress = (e) => {
        if (mode === 'input') {
            // Allow only numbers 1-9
            if (e.key >= '1' && e.key <= '9') {
                setValue(e.key);
                updatePuzzle(e.key, rowIndex, colIndex);
            }
        } else if (mode === 'sketch') {
            // Append to sketch string, allow only numbers, max 9 characters
            const newSketch = (sketch + e.key).slice(0, 9).replace(/[^1-9]/g, '');
            setSketch(newSketch);
        }
        e.preventDefault();  // Prevent the default input behavior
    };

    const switchMode = () => {
        setMode(mode === 'input' ? 'sketch' : 'input');
    };

    return (
        <div className={`cell ${mode}`} onClick={switchMode}>
            {value ? <span className="value">{value}</span> : <span className="sketch">{sketch}</span>}
            <input type="text" value="" onKeyDown={handleKeyPress} />
        </div>
    );
}

export default Cell;


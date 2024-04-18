import React from 'react';

function Cell({ value, onChange, isBlockBorder }) {
  return (
    <div className={`cell ${isBlockBorder ? 'block' : ''}`}>
      <input
        type="text"
        value={value}
        onChange={e => onChange(e.target.value.replace(/[^1-9]/g, ''))}
        maxLength="1"
      />
    </div>
  );
}

export default Cell;


let grid = [];
let isRunning = false;

const ROWS = 20;
const COLS = 30;
const START = { row: 2, col: 2 };
const GOAL = { row: 17, col: 27 };

// Initialize the grid on page load
function initGrid() {
    const gridEl = document.getElementById('grid');
    gridEl.style.gridTemplateColumns = `repeat(${COLS}, 30px)`;
    gridEl.innerHTML = '';

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement('div');
            cell.id = `cell-${r}-${c}`;
            cell.className = 'cell cell-empty';
            gridEl.appendChild(cell);
        }
    }
    fetchGrid();
}

// Fetch grid from Flask backend
function fetchGrid() {
    fetch('/api/grid')
        .then(r => r.json())
        .then(data => {
            grid = data.grid;
            renderGrid();
        });
}

// Render the grid cells
function renderGrid() {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.getElementById(`cell-${r}-${c}`);
            const val = grid[r][c];

            cell.className = 'cell';
            if (r === START.row && c === START.col) {
                cell.className += ' cell-start';
                cell.textContent = '';
            } else if (r === GOAL.row && c === GOAL.col) {
                cell.className += ' cell-goal';
                cell.textContent = '';
            } else if (val === 1) {
                cell.className += ' cell-wall';
                cell.textContent = '';
            } else if (val === 4) {
                cell.className += ' cell-visited';
                cell.textContent = '';
            } else if (val === 5) {
                cell.className += ' cell-path';
                cell.textContent = '';
            } else {
                cell.className += ' cell-empty';
                cell.textContent = '';
            }
        }
    }
}

// Run selected algorithm
async function runAlgorithm() {
    if (isRunning) return;
    isRunning = true;

    const algorithm = document.getElementById('algorithmSelect').value;

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm })
        });

        const data = await response.json();

        for (const [r, c] of data.visited) {
            grid[r][c] = 4;
            renderGrid();
            await new Promise(r => setTimeout(r, 10));
        }

        for (const [r, c] of data.path) {
            grid[r][c] = 5;
            renderGrid();
            await new Promise(r => setTimeout(r, 30));
        }

        document.getElementById('nodesExplored').textContent = data.stats.nodes_explored;
        document.getElementById('pathLength').textContent = data.stats.path_length;
        document.getElementById('time').textContent = data.stats.time.toFixed(2) + 'ms';
    } catch (err) {
        console.error('Error:', err);
    }

    isRunning = false;
}

// Reset grid
function resetGrid() {
    fetch('/api/reset').then(() => fetchGrid());
    document.getElementById('nodesExplored').textContent = '0';
    document.getElementById('pathLength').textContent = '0';
    document.getElementById('time').textContent = '0ms';
}

// Generate new maze
function generateMaze() {
    fetch('/api/generate-maze').then(() => fetchGrid());
}

// Initialize grid on page load
initGrid();

document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const status = document.getElementById('status');
    const resetButton = document.getElementById('reset');

    cells.forEach(cell => {
        cell.addEventListener('click', handleMove);
    });

    resetButton.addEventListener('click', resetGame);

    async function handleMove(e) {
        const cell = e.target;
        const position = cell.dataset.index;

        const response = await fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ position: position })
        });

        const data = await response.json();

        if (data.success) {
            updateBoard(data.board);
            
            if (data.winner) {
                status.textContent = `Player ${data.winner} wins!`;
            } else if (data.isDraw) {
                status.textContent = "It's a draw!";
            } else {
                status.textContent = `Current Player: ${data.currentPlayer}`;
            }
        }
    }

    async function resetGame() {
        const response = await fetch('/reset', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            updateBoard(data.board);
            status.textContent = 'Current Player: X';
        }
    }

    function updateBoard(board) {
        cells.forEach((cell, index) => {
            cell.textContent = board[index];
        });
    }
});
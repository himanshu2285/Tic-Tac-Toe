from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Game state
board = ['' for _ in range(9)]
current_player = 'X'

def check_winner():
    # Winning combinations
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    
    for line in lines:
        if board[line[0]] and board[line[0]] == board[line[1]] == board[line[2]]:
            return board[line[0]]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    global current_player
    position = int(request.json['position'])
    
    if board[position] == '':
        board[position] = current_player
        winner = check_winner()
        is_draw = '' not in board and not winner
        
        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'
        
        return jsonify({
            'success': True,
            'board': board,
            'currentPlayer': current_player,
            'winner': winner,
            'isDraw': is_draw
        })
    
    return jsonify({'success': False})

@app.route('/reset', methods=['POST'])
def reset_game():
    global board, current_player
    board = ['' for _ in range(9)]
    current_player = 'X'
    return jsonify({'success': True, 'board': board})

if __name__ == '__main__':
    app.run(debug=True)
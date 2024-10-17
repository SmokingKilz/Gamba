from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

# Initialize the player's balance
@app.before_request
def initialize_balance():
    if 'balance' not in session:
        session['balance'] = 100  # Start with 100 coins

# Coinflip logic: randomly choose between 'CT' (Counter-Terrorist) or 'T' (Terrorist)
def coinflip():
    return random.choice(["CT", "T"])

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Route for playing the coinflip game
@app.route('/play_coinflip', methods=['POST'])
def play_coinflip():
    user_choice = request.form['choice']
    wager = int(request.form['wager'])  # Get the wager from the form
    bot_choice = coinflip()

    # Ensure the player has enough balance to wager
    if session['balance'] >= wager:
        if user_choice == bot_choice:
            session['balance'] += wager  # Player wins, double their wager
            result = "win"
        else:
            session['balance'] -= wager  # Player loses the wagered amount
            result = "lose"
    else:
        result = "not enough balance"

    return jsonify({
        'bot_choice': bot_choice,
        'result': result,
        'balance': session['balance']
    })

# Route to add 100 coins (debug button functionality)
@app.route('/add_coins', methods=['POST'])
def add_coins():
    session['balance'] += 100
    return jsonify({'balance': session['balance']})

if __name__ == '__main__':
    app.run(debug=True)


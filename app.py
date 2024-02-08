from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Замініть 'YOUR_APPLICATION_ID' на свій application_id, отриманий від Wargaming API
APPLICATION_ID = 'd889298af2382fa0cfeb010e26874b63'
WOT_API_URL = 'https://api.worldoftanks.eu/wot'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_player():
    player_name = request.form.get('player_name')

    if not player_name:
        return render_template('index.html', error='Please enter a player name.')

    player_data = get_player_data(player_name)
    
    if 'error' in player_data:
        return render_template('index.html', error=f"Error: {player_data['error']['message']}")

    return render_template('result.html', player_data=player_data)

def get_player_data(player_name):
    # Отримання даних гравця за його ім'ям
    params = {
        'application_id': APPLICATION_ID,
        'search': player_name
    }

    response = requests.get(f'{WOT_API_URL}/account/list/', params=params)
    data = response.json()

    if data['status'] == 'ok' and data['meta']['count'] > 0:
        account_id = data['data'][0]['account_id']
        player_stats = get_player_stats(account_id)
        return player_stats
    else:
        return {'error': data['error']}

def get_player_stats(account_id):
    # Отримання статистики гравця за його account_id
    params = {
        'application_id': APPLICATION_ID,
        'account_id': account_id
    }

    response = requests.get(f'{WOT_API_URL}/account/info/', params=params)
    data = response.json()

    if data['status'] == 'ok':
        return data['data'][str(account_id)]
    else:
        return {'error': data['error']}

if __name__ == '__main__':
    app.run(debug=True)

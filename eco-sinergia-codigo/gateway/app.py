from flask import Flask, jsonify, request, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        player = requests.get('http://player_service:8001/player').json()
        city = requests.get('http://city_service:8002/city').json()
        ai = requests.post('http://ai_service:8003/analyze', json={'city': city}).json()
        rec = requests.post('http://recommendation_service:8004/recommend', json={'city': city, 'ai': ai}).json()
        return jsonify({'player': player, 'city': city, 'ai_reaction': ai, 'recommendation': rec})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

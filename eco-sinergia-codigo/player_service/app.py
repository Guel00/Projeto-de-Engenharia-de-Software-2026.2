from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/player', methods=['GET'])
def get_player():
    return jsonify({"level": 5, "money": 1500, "name": "Gestor Ambiental"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

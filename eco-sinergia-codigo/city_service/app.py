from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/city', methods=['GET'])
def get_city():
    return jsonify({"trees": 120, "buildings": 45, "pollution": 35})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)

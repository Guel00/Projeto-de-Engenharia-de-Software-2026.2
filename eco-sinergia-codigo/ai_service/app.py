from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    pollution = data.get('city', {}).get('pollution', 0)
    
    happiness = 100 - (pollution * 1.5)
    feedback = "A população está respirando bem!" if pollution < 50 else "A população está sofrendo com alergias e poluição!"
    
    return jsonify({"happiness_impact": max(0, happiness), "feedback": feedback})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)

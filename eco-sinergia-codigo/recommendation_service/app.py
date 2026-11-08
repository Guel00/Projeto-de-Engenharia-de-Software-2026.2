from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    city = data.get('city', {})
    
    if city.get('pollution', 0) > 40:
        tip = "Urgente: Construa mais parques e plante árvores para reduzir a poluição!"
    elif city.get('trees', 0) < city.get('buildings', 0):
        tip = "Atenção: Você tem mais prédios do que árvores. Equilibre a natureza."
    else:
        tip = "Excelente trabalho! Continue mantendo o equilíbrio sustentável."
        
    return jsonify({"tip": tip})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)

# meu_projeto_flask/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Olá, Flask! Esta é a API de exemplo.")

@app.route('/saudacao/<string:nome>')
def saudacao(nome):
    if not nome:
        return jsonify(error="Nome não fornecido"), 400
    return jsonify(message=f"Olá, {nome}!")

@app.route('/somar', methods=['POST'])
def somar():
    data = request.get_json()
    if not data or 'num1' not in data or 'num2' not in data:
        return jsonify(error="Faltam números para a soma"), 400
    try:
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        resultado = num1 + num2
        return jsonify(resultado=resultado)
    except ValueError:
        return jsonify(error="Entradas inválidas para soma"), 400

if __name__ == '__main__':
    app.run(debug=True)
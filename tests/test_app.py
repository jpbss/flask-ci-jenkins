import pytest
from app import app

@pytest.fixture
def client():
    # Configura o cliente de teste para a aplicação Flask
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    # Testa se a rota inicial retorna a mensagem esperada e status 200
    response = client.get('/')
    assert response.status_code == 200
    assert "Olá, Flask!" in response.get_json()['message']

def test_saudacao_com_nome(client):
    # Testa a rota /saudacao com um nome válido
    response = client.get('/saudacao/Mundo')
    assert response.status_code == 200
    assert "Olá, Mundo!" in response.get_json()['message']

def test_saudacao_sem_nome(client):
    # Testa a rota /saudacao sem nome (deve dar erro 400)
    response = client.get('/saudacao/') # Rota sem nome, Flask deve retornar 404 por default se não houver rota específica para isso
    assert response.status_code == 404 # Esperamos 404 aqui porque '/saudacao/' não é '/saudacao/<nome>'

def test_somar_valido(client):
    # Testa a rota /somar com números válidos
    response = client.post('/somar', json={'num1': 5, 'num2': 3})
    assert response.status_code == 200
    assert response.get_json()['resultado'] == 8.0

def test_somar_faltando_parametros(client):
    # Testa a rota /somar sem todos os parâmetros
    response = client.post('/somar', json={'num1': 5})
    assert response.status_code == 400
    assert "Faltam números para a soma" in response.get_json()['error']

def test_somar_parametros_invalidos(client):
    # Testa a rota /somar com parâmetros não numéricos
    response = client.post('/somar', json={'num1': 'abc', 'num2': 3})
    assert response.status_code == 400
    assert "Entradas inválidas para soma" in response.get_json()['error']
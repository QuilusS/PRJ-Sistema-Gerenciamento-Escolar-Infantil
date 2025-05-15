import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.crudAlunos import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('Util.bd.create_connection')
def test_create_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/alunos', json={
        'aluno_id': 1,
        'nome': 'Teste Aluno',
        'endereco': 'Rua A',
        'cidade': 'Cidade X',
        'estado': 'SP',
        'cep': '12345-678',
        'pais': 'Brasil',
        'telefone': '123456789'
    })

    assert response.status_code == 201
    assert b'Aluno criado com sucesso' in response.data

@patch('Util.bd.create_connection')
def test_create_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/alunos', json={
        'aluno_id': 1,
        'nome': 'Teste Aluno',
        'endereco': 'Rua A',
        'cidade': 'Cidade X',
        'estado': 'SP',
        'cep': '12345-678',
        'pais': 'Brasil',
        'telefone': '123456789'
    })

    assert response.status_code == 500
    assert b'Falha ao conectar ao banco' in response.data

@patch('Util.bd.create_connection')
def test_read_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 'Teste Aluno', 'Rua A', 'Cidade X', 'SP', '12345-678', 'Brasil', '123456789')

    response = client.get('/alunos/1')

    assert response.status_code == 200
    assert b'Teste Aluno' in response.data

@patch('Util.bd.create_connection')
def test_read_aluno_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get('/alunos/1')

    assert response.status_code == 404
    assert "Aluno não encontrado" in response.data.decode('utf-8')

@patch('Util.bd.create_connection')
def test_update_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put('/alunos/1', json={
        'nome': 'Teste Aluno Atualizado',
        'endereco': 'Rua B',
        'cidade': 'Cidade Y',
        'estado': 'RJ',
        'cep': '87654-321',
        'pais': 'Brasil',
        'telefone': '987654321'
    })

    assert response.status_code == 200
    assert b'Aluno atualizado com sucesso' in response.data

@patch('Util.bd.create_connection')
def test_delete_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete('/alunos/1')

    assert response.status_code == 200
    assert b'Aluno deletado com sucesso' in response.data
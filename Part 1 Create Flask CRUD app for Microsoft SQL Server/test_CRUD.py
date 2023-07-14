import sys
sys.path.append("..")
from app import create_bank, list_banks, get_bank, update_bank, delete_bank
from app import app
import pytest
from flask import Flask
import pyodbc
import requests
from unittest.mock import MagicMock

# Mock the database connection
class MockDBConnection:
    def __init__(self):
        self.data = [
            {'id': 1, 'name': 'Bank A', 'location': 'Location A'},
            {'id': 2, 'name': 'Bank B', 'location': 'Location B'}
        ]

    def execute(self, query, params=None):
        if query.startswith('SELECT'):
            # Get all banks or a specific bank by ID
            if params:
                bank_id = params[0]
                return [bank for bank in self.data if bank['id'] == bank_id]
            else:
                return self.data
        elif query.startswith('INSERT'):
            # Create a new bank record
            new_bank = {'id': len(self.data) + 1, 'name': params[0], 'location': params[1]}
            self.data.append(new_bank)
            return new_bank
        elif query.startswith('UPDATE'):
            # Update a bank record
            bank_id, name, location = params
            for bank in self.data:
                if bank['id'] == bank_id:
                    bank['name'] = name
                    bank['location'] = location
                    return bank
            return None
        elif query.startswith('DELETE'):
            # Delete a bank record
            bank_id = params[0]
            for bank in self.data:
                if bank['id'] == bank_id:
                    self.data.remove(bank)
                    break
            return None

@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Patch the database connection to use the mock
    app.config['DB_CONNECTION'] = MockDBConnection()

    with app.test_client() as client:
        yield client


def test_create_bank(client, monkeypatch):

    # Mock the database connection and cursor objects
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    monkeypatch.setattr('pyodbc.connect', lambda _: mock_conn)
    monkeypatch.setattr('pyodbc.Cursor', lambda *_: mock_cursor)

    data = {
        'id': '123',
        'name': 'My Bank',
        'location': 'City'
    }

    response = client.post('/create', data=data)

    assert response.status_code == 200
    assert b"Record created successfully!" in response.data



def test_list_banks(client):
    # Send a GET request to retrieve the list of banks
    # Make a GET request to the /banks route
    response = client.get('/banks')

    assert response.status_code == 200
    assert b"List of Banks" in response.data


def test_get_bank(client):
    # Make a GET request to the /banks/<bank_id> route
    bank_id = 1
    response = client.get(f'/banks/{bank_id}')

    assert response.status_code == 200
    assert b"ABC Bank" in response.data
    assert b"New York" in response.data


def test_update_bank(client):
    # Send a PUT request to update a bank's record
    response = client.put('/banks/1', json={'name': 'Bank X', 'location': 'Location X'})

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Bank X'
    assert data['location'] == 'Location X'

def test_delete_bank(client, monkeypatch):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    monkeypatch.setattr('pyodbc.connect', lambda _: mock_conn)
    monkeypatch.setattr('pyodbc.Cursor', lambda *_: mock_cursor)

    # Make a POST request to the /deletebank/<bank_id> route
    bank_id = 1
    response = client.delete(f'/deletebank/{bank_id}')

    assert response.status_code == 200
    assert b"Bank deleted successfully!" in response.data
    # Send a DELETE request to delete a bank record
    #response = client.delete('/banks/1')

    # Check the response status code

    # Check that the bank record was deleted
    response = client.get('/banks/1')
    assert response.status_code == 204


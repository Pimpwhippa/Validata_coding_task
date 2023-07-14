import pyodbc
import pytest
import requests
from app import app
from flask import Flask
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

    # sending data to create a record
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
    bank_id = 2
    response = client.get(f'/banks/{bank_id}')

    assert response.status_code == 200
    assert b"Billionaire Bank" in response.data
    assert b"Dublin" in response.data


def test_update_bank(client,monkeypatch):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    monkeypatch.setattr('pyodbc.connect', lambda _: mock_conn)
    monkeypatch.setattr('pyodbc.Cursor', lambda *_: mock_cursor)

    # send data to update a record
    data = {
        'id': '123',
        'name': 'My Bank',
        'location': 'City'
    }
        
    # Make a POST request to the /updatebank route
    response = client.post('/updatebank', data=data)

    assert response.status_code == 200
    assert response.data == b"Bank record updated successfully!"


def test_delete_bank(client, monkeypatch):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    monkeypatch.setattr('pyodbc.connect', lambda _: mock_conn)
    monkeypatch.setattr('pyodbc.Cursor', lambda *_: mock_cursor)

    # Make a POST request to the /deletebank/<bank_id> route
    bank_id = 1
    response = client.post('/deletebank/1')
   
    # Check the response status code
    assert response.status_code == 200
    assert response.data == b"Bank deleted successfully!"
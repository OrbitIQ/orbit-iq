import pytest
from app import app, get_db_connection

# This fixture will be used by the tests to send requests to the application
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_satellites(client):
    """Test getting all satellites without pagination."""
    response = client.get('/confirmed/satellites')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data

def test_get_satellites_with_pagination(client):
    """Test getting satellites with pagination."""
    response = client.get('/confirmed/satellites?limit=5&page=2')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data
    assert len(data['satellites']) == 5

def test_database_connection():
    """Test database connection."""
    conn = get_db_connection()
    assert conn is not None
    conn.close()

def test_cors_headers(client):
    """Test CORS headers are set correctly."""
    response = client.get('/confirmed/satellites')
    assert response.headers['Access-Control-Allow-Origin'] == '*'
    assert 'Content-Type' in response.headers['Access-Control-Allow-Headers']
    assert 'Authorization' in response.headers['Access-Control-Allow-Headers']

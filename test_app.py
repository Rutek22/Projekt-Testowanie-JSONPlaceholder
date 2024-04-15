import pytest
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client





def test_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200



def test_get_albums(client):
    response = client.get('/albums')
    assert response.status_code == 200



def test_get_photos(client):
    response = client.get('/albums/1/photos/albumTitle')
    assert response.status_code == 200







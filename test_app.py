import pytest
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_posts_page(client):
    response = client.get('/posts')
    assert response.status_code == 200


def test_albums_page(client):
    response = client.get('/albums')
    assert response.status_code == 200


def test_photos_page(client):
    response = client.get('/albums/1/photos/albumTitle')
    assert response.status_code == 200

import pytest
import requests
from main import app

API_URL = 'https://jsonplaceholder.typicode.com/'

"""
Testy te sprawdzają czy odwołanie się do poszczególnych endpointów
zwraca odpowiedź HTTP o kodzie statusu 200
 i czy w treści odpowiedzi znajduje się fraza
(Albumy, Zdjęcia, Posty)
"""


@pytest.mark.contract
def test_get_albums():
    response = app.test_client().get('/albums')

    # Sprawdzenie statusu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formatu danych (Content-Type)
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Sprawdzenie zawartości odpowiedzi
    assert b'Albumy' in response.data
    assert b'albums' in response.data
    assert b'photos' in response.data
    assert b'limit' in response.data


@pytest.mark.contract
def test_get_albums_with_limit():
    response = app.test_client().get('/albums/5')

    # Sprawdzenie statusu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formatu danych (Content-Type)
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Sprawdzenie zawartości odpowiedzi
    assert b'Albumy' in response.data
    assert b'albums' in response.data
    assert b'photos' in response.data
    assert b'limit' in response.data


@pytest.mark.contract
def test_get_photos():
    response = app.test_client().get('/albums/1/photos/album_title')

    # Sprawdzenie statusu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formatu danych (Content-Type)
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Sprawdzenie zawartości odpowiedzi
    assert 'Zdjęcia'.encode('utf-8') in response.data
    assert b'photos' in response.data
    assert b'albumId' in response.data
    assert b'albumTitle' in response.data
    assert b'limit' in response.data


@pytest.mark.contract
def test_get_photos_with_limit():
    response = app.test_client().get('/albums/1/photos/album_title/5')

    # Sprawdzenie statusu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formatu danych (Content-Type)
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Sprawdzenie zawartości odpowiedzi
    assert 'Zdjęcia'.encode('utf-8') in response.data
    assert b'photos' in response.data
    assert b'albumId' in response.data
    assert b'albumTitle' in response.data
    assert b'limit' in response.data


@pytest.mark.contract
def test_get_posts():
    response = app.test_client().get('/posts')

    # Sprawdzenie statusu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formatu danych (Content-Type)
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Sprawdzenie zawartości odpowiedzi
    assert b'Posts' in response.data
    assert b'posts' in response.data
    assert b'comments' in response.data
    assert b'limit_posts' in response.data
    assert b'limit_comments' in response.data
    assert b'min_chars' in response.data
    assert b'max_chars' in response.data


@pytest.mark.contract
def test_get_posts_with_limit():
    response = app.test_client().get('/posts/5/5')

    # Sprawdzenie statusu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formatu danych (Content-Type)
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

    # Sprawdzenie zawartości odpowiedzi
    assert b'Posts' in response.data
    assert b'Posts' in response.data
    assert b'posts' in response.data
    assert b'comments' in response.data
    assert b'limit_posts' in response.data
    assert b'limit_comments' in response.data
    assert b'min_chars' in response.data
    assert b'max_chars' in response.data


@pytest.mark.contract
def test_css_contract():
    # Adres URL, z którego pobieramy plik CSS
    css_url = ('https://raw.githubusercontent.com/'
               'Rutek22/Projekt-Testowanie'
               '-JSONPlaceholder/'
               '0b551f4e1ce5a408c7c5'
               '69354dbf966e8f2318cf/'
               'static/css/main.css')

    # Wywołanie zapytania HTTP GET w celu pobrania pliku CSS
    response = requests.get(css_url)

    # Sprawdzenie, czy odpowiedź serwera ma kod statusu 200 (OK)
    assert response.status_code == 200, "Failed to retrieve CSS file"

    # Sprawdzenie, czy treść odpowiedzi zawiera poprawne znaczniki CSS
    css_tags = ['p', 'h1', 'h2', 'h3', 'a', 'ul', 'ol', 'li']
    response_text = response.text.lower()
    missing_tags = [tag for tag in css_tags if tag not in response_text]

    # Wypisanie brakujących znaczników CSS
    if missing_tags:
        print("Missing CSS tags:", missing_tags)

    # Sprawdzenie, czy nie ma brakujących znaczników
    assert not missing_tags, "Content does not contain CSS tags"

import time
import requests

# Adres lokalny aplikacji Flask
BASE_URL = 'http://127.0.0.1:5000/'

# Test wydajnościowy dla strony głównej
def test_index_page():
    start_time = time.time()
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print("Czas odpowiedzi strony głównej:", time.time() - start_time, "sekund")

# Test wydajnościowy dla strony z postami
def test_posts_page():
    start_time = time.time()
    response = requests.get(BASE_URL + 'posts')
    assert response.status_code == 200
    assert "Posty" in response.text
    print("Czas odpowiedzi strony postów:", time.time() - start_time, "sekund")

# Test wydajnościowy dla strony z albumami
def test_albums_page():
    start_time = time.time()
    response = requests.get(BASE_URL + 'albums')
    assert response.status_code == 200
    assert "Albumy" in response.text
    print("Czas odpowiedzi strony albumów:", time.time() - start_time, "sekund")

# Test wydajnościowy dla strony z zdjęciami dla danego albumu
def test_photos_page():
    album_id = 1  # ID albumu do przetestowania
    album_title = 'example_title'  # Tytuł albumu
    start_time = time.time()
    response = requests.get(BASE_URL + f'albums/{album_id}/photos/{album_title}')
    assert response.status_code == 200
    assert "Zdjęcia" in response.text
    print("Czas odpowiedzi strony zdjęć dla albumu:", time.time() - start_time, "sekund")

# Uruchomienie testów
if __name__ == "__main__":
    test_index_page()
    test_posts_page()
    test_albums_page()
    test_photos_page()

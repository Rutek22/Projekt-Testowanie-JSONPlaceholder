# Potrzebne biblioteki
from flask import Flask, render_template, request, jsonify
import requests
import logging
from logging.handlers import RotatingFileHandler


# Utworzenie obiektu aplikacji Flask
app = Flask(__name__)


# Adres API JSONPlaceholder
API_URL = 'https://jsonplaceholder.typicode.com/'


# Konfiguracja obsługi logowania do pliku
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)


# Ustawienie poziomu logowania na ERROR, aby logować tylko błędy
handler.setLevel(logging.ERROR)
formatter =\
    (logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
handler.setFormatter(formatter)
app.logger.addHandler(handler)


# Obsługa błędów 404
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Strona nie znaleziona: %s', e)
    return render_template('404.html'), 404


# Obsługa błędów 500
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('Wewnętrzny błąd serwera: %s', e)
    return render_template('500.html'), 500


# Strona index.html
@app.route('/')
def index():
    return render_template("index.html")


# Strona posts.html
@app.route('/posts')
def getPosts():
    limit_posts = 100  # Domyślny limit ustawiony na 100 dla postów

    # Pobranie danych o postach
    response = requests.get(API_URL + 'posts')
    posts = response.json()[:limit_posts]

    limit_comments = 2  # Domyślny limit ustawiony na 2 dla komentarzy

    # Pobranie komentarzy dla postow
    response_comments = requests.get(API_URL + 'comments')
    comments = response_comments.json()

    # Domyślnie minimalna liczba znaków to 0
    min_chars = request.args.get('min_chars', default=0, type=int)

    # Domyślnie maksymalna liczba znaków to 100
    max_chars = request.args.get('max_chars', default=500, type=int)

    return render_template("posts.html",
                           posts=posts,
                           comments=comments,
                           limit_posts=limit_posts,
                           limit_comments=limit_comments,
                           min_chars=min_chars,
                           max_chars=max_chars)


# Strona posts.html z ustawionymi limitami
@app.route('/posts/<int:limit_posts>/<int:limit_comments>')
def getPostsWithLimit(limit_posts, limit_comments):
    # Pobranie minimalnej liczby znaków z parametru URL
    min_chars = request.args.get('min_chars')

    # Pobranie maksymalnej liczby znaków z parametru URL
    max_chars = request.args.get('max_chars')

    # Pobranie danych o postach
    response = requests.get(API_URL + 'posts')
    posts = response.json()[:100]

    # Pobranie komentarzy dla postow
    response_comments = requests.get(API_URL + 'comments')
    comments = response_comments.json()

    # Filtrowanie postów na podstawie liczby znaków w treści
    if min_chars is not None and max_chars is not None:
        try:
            min_chars = int(min_chars)
            max_chars = int(max_chars)
            posts = [post for post in posts if min_chars <= len(post['body']) <= max_chars]
        except ValueError:
            return \
                (jsonify
                 ({'error': "Invalid min_chars or max_chars values"}), 400)

    return render_template("posts.html",
                           posts=posts[:limit_posts],
                           comments=comments,
                           limit_posts=limit_posts,
                           limit_comments=limit_comments,
                           min_chars=min_chars,
                           max_chars=max_chars)


# Strona albums.html
@app.route('/albums')
def getAlbums():
    limit = 10  # Domyślny limit ustawiony na 10

    # Pobranie danych o albumach
    response = requests.get(API_URL + 'albums')
    albums = response.json()[:limit]  # Pobierz tylko pierwszych 10 albumów

    # Pobranie danych o zdjęciach
    response_photos = requests.get(API_URL + 'photos')
    photos = response_photos.json()

    return render_template("albums.html",
                           albums=albums,
                           photos=photos,
                           limit=limit)


# Strona albums.html z ustawionym limitem
@app.route('/albums/<int:limit>')
def getAlbumsWithLimit(limit):
    # Pobranie danych o albumach
    response = requests.get(API_URL + 'albums')
    albums = response.json()[:limit]  # Pobierz tylko określoną liczbę albumów

    # Pobranie danych o zdjęciach
    response_photos = requests.get(API_URL + 'photos')
    photos = response_photos.json()

    return render_template("albums.html",
                           albums=albums,
                           photos=photos,
                           limit=limit)


# Strona photos.html dla wybranego albumu
@app.route('/albums/<int:albumId>/photos/<albumTitle>')
def getPhotos(albumId, albumTitle):
    limit = 10  # Domyślny limit ustawiony na 10

    # Pobranie zdjęć dla danego albumu
    response = requests.get(API_URL + 'photos', params={'albumId': albumId})
    photos = response.json()[:limit]  # Pierwsze 10 zdjęć

    return render_template("photos.html",
                           photos=photos,
                           albumId=albumId,
                           albumTitle=albumTitle,
                           limit=limit)


# Strona photos.html dla wybranego albumu z ustawionym limitem
@app.route('/albums/<int:albumId>/photos/<albumTitle>/<int:limit>')
def getPhotosWithLimit(albumId, albumTitle, limit):
    # Pobranie zdjęć dla danego albumu
    response = requests.get(API_URL + 'photos', params={'albumId': albumId})
    photos = response.json()[:limit]

    return render_template("photos.html",
                           photos=photos,
                           albumId=albumId,
                           albumTitle=albumTitle,
                           limit=limit)

# Uruchomienie aplikacji
if __name__ == '__main__':
    print("http://127.0.0.1:5000/")
    app.run(debug=True)

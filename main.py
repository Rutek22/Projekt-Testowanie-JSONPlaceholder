# Biblioteki
from flask import Flask, render_template
import requests


# Utworzenie obiektu aplikacji Flask
app = Flask(__name__)


# Adres API JSONPlaceholder
API_URL = 'https://jsonplaceholder.typicode.com/'


@app.route('/')
def index():
    return render_template("index.html")


# /posts - posts.html
@app.route('/posts')
def getPosts():
    limit_posts = 10  # Domyślny limit ustawiony na 10 dla postów
    # Pobranie danych o postach
    response = requests.get(API_URL + 'posts')
    posts = response.json()[:limit_posts]

    limit_comments = 2  # Domyślny limit ustawiony na 2 dla komentarzy
    # Pobranie komentarzy dla postow
    response_comments = requests.get(API_URL + 'comments')
    comments = response_comments.json()

    return render_template("posts.html",
                           posts=posts,
                           comments=comments,
                           limit_posts=limit_posts,
                           limit_comments=limit_comments)


@app.route('/posts/<int:limit_posts>/<int:limit_comments>')
def getPostsWithLimit(limit_posts, limit_comments):
    # Pobranie danych o postach
    response = requests.get(API_URL + 'posts')
    posts = response.json()[:limit_posts]

    # Pobranie komentarzy dla postow
    response_comments = requests.get(API_URL + 'comments')
    comments = response_comments.json()

    return render_template("posts.html",
                           posts=posts,
                           comments=comments,
                           limit_posts=limit_posts,
                           limit_comments=limit_comments)


# /albums - albums.html
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


# /albums/<int:albumId>/photos - photos.html
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

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import requests
from flask import Flask
from main import app, API_URL

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_app_exists(self):
        self.assertIsNotNone(app, "Application instance does not exist")

    def test_app_instance(self):
        self.assertIsInstance(app, Flask,
                              "Application is not an instance of Flask")

    def test_api_url_exists(self):
        self.assertIsNotNone(API_URL, "API URL is not defined")

    def test_api_url_valid(self):
        expected_url = 'https://jsonplaceholder.typicode.com/'
        self.assertEqual(API_URL, expected_url, "API URL is not correct")

    def test_index(self):
        with app.test_request_context('/'):
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_getAlbums(self, mocked_get):
        # Symuluj odpowiedź zapytania o albumy
        mocked_albums_response = MagicMock()
        mocked_albums_response.json.return_value = [{'id': 1,
                                                     'title': 'Album 1'},
                                                    {'id': 2,
                                                     'title': 'Album 2'}]
        # Symuluj odpowiedź zapytania o zdjęcia
        mocked_photos_response = MagicMock()
        mocked_photos_response.json.return_value = [{'albumId': 1,
                                                     'title': 'Photo 1'},
                                                    {'albumId': 2,
                                                     'title': 'Photo 2'}]
        # Ustaw efekt dla każdego wywołania z requests.get
        mocked_get.side_effect = [mocked_albums_response,
                                  mocked_photos_response]

        # Wywołaj funkcję getAlbums()
        with app.test_request_context('/albums'):
            response = self.app.get('/albums')

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Album 1', response.data)
            self.assertIn(b'Album 2', response.data)
            self.assertIn(b'Photo 1', response.data)
            self.assertIn(b'Photo 2', response.data)

    def test_getAlbumsWithLimit(self):
        with patch('main.requests.get') as mocked_get:
            mocked_albums_response = MagicMock()
            mocked_albums_response.json.return_value = [{'id': 1,
                                                         'title':
                                                             'Album 1'},
                                                        {'id': 2,
                                                         'title':
                                                             'Album 2'}]
            mocked_get.return_value = mocked_albums_response

            response = self.app.get('/albums/2')

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Album 1', response.data)
            self.assertIn(b'Album 2', response.data)

    @patch('requests.get')
    def test_getPhotos(self, mocked_get):
        # Symuluj odpowiedź zapytania o zdjęcia dla albumu o id 1
        mocked_photos_response = MagicMock()
        mocked_photos_response.json.return_value = [{'id': 1, 'albumId': 1,
                                                     'title': 'Photo 1'},
                                                    {'id': 2, 'albumId': 1,
                                                     'title': 'Photo 2'}]
        mocked_get.return_value = mocked_photos_response

        # Wywołaj funkcję getPhotos()
        with app.test_request_context('/albums/1/photos/Album 1'):
            response = self.app.get('/albums/1/photos/Album 1')

            # Sprawdź, czy odpowiedź ma status kodu 200
            self.assertEqual(response.status_code, 200)

            # Sprawdź, czy dane o zdjęciach dla albumu są obecne
            self.assertIn(b'Photo 1', response.data)
            self.assertIn(b'Photo 2', response.data)

    @patch('requests.get')
    def test_getPhotosWithLimit(self, mocked_get):
        mocked_photos_response = MagicMock()
        mocked_photos_response.json.return_value = [{'id': 1, 'albumId': 1,
                                                     'title': 'Photo 1'},
                                                    {'id': 2, 'albumId': 1,
                                                     'title': 'Photo 2'}]
        mocked_get.return_value = mocked_photos_response

        # Wywołaj funkcję getPhotosWithLimit()
        with app.test_request_context('/albums/1/photos/Album 1/2'):
            response = self.app.get('/albums/1/photos/Album 1/2')

            # Sprawdź, czy odpowiedź ma status kodu 200
            self.assertEqual(response.status_code, 200)

            # Sprawdź, czy dane o zdjęciach dla albumu z limitem są obecne
            self.assertIn(b'Photo 1', response.data)
            self.assertIn(b'Photo 2', response.data)

    def test_getPosts(self):
        with patch('main.requests.get') as mocked_get:
            # Symuluj odpowiedź zapytania o posty
            mocked_posts_response = MagicMock()
            mocked_posts_response.json.return_value = [{'id': 1,
                                                        'title':
                                                            'Post 1',
                                                        'body':
                                                            'Body post 1'},
                                                       {'id': 2,
                                                        'title':
                                                            'Post 2',
                                                        'body':
                                                            'Body post 2'}]
            # Symuluj odpowiedź zapytania o komentarze
            mocked_comments_response = MagicMock()
            mocked_comments_response.json.return_value = [{'postId': 1,
                                                           'id': 1,
                                                           'body':
                                                               'Comment 1'},
                                                          {'postId': 1,
                                                           'id': 2,
                                                           'body':
                                                               'Comment 2'},
                                                          {'postId': 2,
                                                           'id': 3,
                                                           'body':
                                                               'Comment 3'}]
            # Ustaw efekt dla każdego wywołania z requests.get
            mocked_get.side_effect = [mocked_posts_response,
                                      mocked_comments_response]

            # Wywołaj funkcję getPosts()
            with app.test_request_context('/posts'):
                response = self.app.get('/posts')

                # Sprawdź, czy odpowiedź ma status kodu 200
                self.assertEqual(response.status_code, 200)

                # Sprawdź, czy dane o postach są obecne w treści odpowiedzi
                self.assertIn(b'Post 1', response.data)
                self.assertIn(b'Post 2', response.data)
                self.assertIn(b'Body post 1', response.data)
                self.assertIn(b'Body post 2', response.data)

                # Sprawdź, czy dane o komentarzach są obecne w treści
                self.assertIn(b'Comment 1', response.data)
                self.assertIn(b'Comment 2', response.data)
                self.assertIn(b'Comment 3', response.data)

    def test_getPostsWithLimit(self):
        with patch('main.requests.get') as mocked_get:
            # Symuluj odpowiedź zapytania o posty
            mocked_posts_response = MagicMock()
            mocked_posts_response.json.return_value = [{'id': 1,
                                                        'title':
                                                            'Post 1',
                                                        'body':
                                                            'Body post 1'},
                                                       {'id': 2,
                                                        'title':
                                                            'Post 2',
                                                        'body':
                                                            'Body post 2'}]
            # Symuluj odpowiedź zapytania o komentarze
            mocked_comments_response = MagicMock()
            mocked_comments_response.json.return_value = [{'postId': 1,
                                                           'id': 1,
                                                           'body':
                                                               'Comment 1'},
                                                          {'postId': 1,
                                                           'id': 2,
                                                           'body':
                                                               'Comment 2'},
                                                          {'postId': 2,
                                                           'id': 3,
                                                           'body':
                                                               'Comment 3'}]
            # Ustaw efekt dla każdego wywołania z requests.get
            mocked_get.side_effect = [mocked_posts_response,
                                      mocked_comments_response]

            # Wywołaj funkcję z parametrami limit_posts=2 i limit_comments=2
            with app.test_request_context(
                    '/posts/2/2?min_chars=0&max_chars=500'):
                response = self.app.get('/posts/2/2')

                # Sprawdź, czy odpowiedź ma status kodu 200
                self.assertEqual(response.status_code, 200)

                # Sprawdź, czy odpowiednia liczba postów jest obecna
                self.assertIn(b'Post 1', response.data)
                self.assertIn(b'Post 2', response.data)

                # Sprawdź, czy odpowiednia liczba komentarzy jest obecna
                self.assertIn(b'Comment 1', response.data)
                self.assertIn(b'Comment 2', response.data)
                self.assertIn(b'Comment 3', response.data)

    def test_css_contract(self):
        # Adres URL, z którego pobieramy plik CSS
        css_url = ('https://raw.githubusercontent.com/'
                   'Rutek22/Projekt-Testowanie-JSONPlaceholder/'
                   '0b551f4e1ce5a408c7c569354dbf966e8f2318cf/'
                   'static/css/main.css')

        # Wywołanie zapytania HTTP GET w
        # celu pobrania pliku CSS
        response = requests.get(css_url)

        # Sprawdzenie, czy odpowiedź serwera ma
        # kod statusu 200 (OK)
        self.assertEqual(response.status_code,
                         200, "Failed to retrieve CSS file")


        # Sprawdzenie, czy treść odpowiedzi
        # zawiera poprawne znaczniki CSS
        css_tags = [   'p', 'h1', 'h2', 'h3', 'a', 'ul', 'ol',
                    'li']
        response_text = response.text.lower()
        missing_tags = [tag for tag in css_tags if tag
                        not in response_text]

        # Wypisanie brakujących znaczników CSS
        if missing_tags:
            print("Missing CSS tags:", missing_tags)

        # Sprawdzenie, czy nie ma brakujących znaczników
        self.assertFalse(missing_tags,
                         "Content does not contain CSS tags")



if __name__ == '__main__':
    unittest.main()

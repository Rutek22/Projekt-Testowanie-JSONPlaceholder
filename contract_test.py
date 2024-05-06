import unittest
from flask import Flask
from flask_testing import TestCase
from app import app

class TestHTMLContent(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_homepage(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_posts_page(self):
        response = self.client.get('/posts')
        self.assert200(response)
        self.assert_template_used('posts.html')
        self.assertIn(b'Limit wy\u015bwietlanych post\xc3\xb3w:', response.data)
        self.assertIn(b'Limit wy\u015bwietlanych komentarzy:', response.data)
        self.assertIn(b'Minimalna liczba znak\xc3\xb3w:', response.data)
        self.assertIn(b'Maksymalna liczba znak\xc3\xb3w:', response.data)

if __name__ == '__main__':
    unittest.main()

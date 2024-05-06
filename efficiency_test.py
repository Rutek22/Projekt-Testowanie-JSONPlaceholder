from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_index_page(self):
        response = self.client.get("/")
        assert response.status_code == 200

    @task
    def test_posts_page(self):
        response = self.client.get("/posts")
        assert response.status_code == 200
        assert "Posty" in response.text

    @task
    def test_albums_page(self):
        response = self.client.get("/albums")
        assert response.status_code == 200
        assert "Albumy" in response.text

    @task
    def test_photos_page(self):
        album_id = 1  # ID albumu do przetestowania
        album_title = 'example_title'  # Tytuł albumu
        response = self.client.get(f"/albums/{album_id}/photos/{album_title}")
        assert response.status_code == 200
        assert "Zdjęcia" in response.text


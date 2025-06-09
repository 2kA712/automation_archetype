import pytest
from resources.apis.example_base_api import BaseAPIController


class TestJSONPlaceholderSync:
    """Тестування JSONPlaceholder API (синхронно)"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Налаштування та очищення для кожного тесту"""
        # Налаштування
        self.api = BaseAPIController("https://jsonplaceholder.typicode.com")
        self.api.setup()

        yield

        # Очищення
        self.api.teardown()

    def test_get_all_posts(self):
        """Тест отримання всіх постів"""
        # Виконання запиту
        response = self.api.get("/posts")

        # Перевірки
        assert response['status_code'] == 200, f"Очікувався статус 200, отримано {response['status_code']}"
        assert isinstance(response['data'], list), "Відповідь повинна бути списком"
        assert len(response['data']) > 0, "Список постів не може бути порожнім"

        # Перевірка структури першого поста
        first_post = response['data'][0]
        required_fields = ['id', 'title', 'body', 'userId']

        for field in required_fields:
            assert field in first_post, f"Поле '{field}' відсутнє в пості"

    def test_get_single_post(self):
        """Тест отримання конкретного поста"""
        post_id = 1
        response = self.api.get(f"/posts/{post_id}")

        # Перевірки
        assert response['status_code'] == 200
        assert response['data']['id'] == post_id
        assert 'title' in response['data']
        assert 'body' in response['data']
        assert len(response['data']['title']) > 0, "Заголовок поста не може бути порожнім"

    def test_get_nonexistent_post(self):
        """Тест запиту неіснуючого поста"""
        response = self.api.get("/posts/999999")

        # JSONPlaceholder повертає 404 для неіснуючих ресурсів
        assert response['status_code'] == 404

    def test_create_new_post(self):
        """Тест створення нового поста"""
        new_post_data = {
            'title': 'Тестовий пост',
            'body': 'Це тестовий пост створений автоматизованим тестом',
            'userId': 1
        }

        response = self.api.post("/posts", data=new_post_data)

        # Перевірки
        assert response['status_code'] == 201  # Created
        assert response['data']['title'] == new_post_data['title']
        assert response['data']['body'] == new_post_data['body']
        assert response['data']['userId'] == new_post_data['userId']
        assert 'id' in response['data'], "Новий пост повинен мати ID"

    def test_update_post(self):
        """Тест оновлення поста"""
        post_id = 1
        updated_data = {
            'id': post_id,
            'title': 'Оновлений заголовок',
            'body': 'Оновлений текст поста',
            'userId': 1
        }

        response = self.api.put(f"/posts/{post_id}", data=updated_data)

        # Перевірки
        assert response['status_code'] == 200
        assert response['data']['title'] == updated_data['title']
        assert response['data']['body'] == updated_data['body']

    def test_delete_post(self):
        """Тест видалення поста"""
        post_id = 1
        response = self.api.delete(f"/posts/{post_id}")

        # JSONPlaceholder повертає 200 для видалення
        assert response['status_code'] == 200

    def test_get_posts_with_query_params(self):
        """Тест використання query параметрів"""
        params = {'userId': 1}
        response = self.api.get("/posts", params=params)

        # Перевірки
        assert response['status_code'] == 200
        assert len(response['data']) > 0

        # Всі пости повинні належати користувачу з ID = 1
        for post in response['data']:
            assert post['userId'] == 1

    def test_response_headers(self):
        """Тест перевірки заголовків відповіді"""
        response = self.api.get("/posts/1")

        # Перевірка наявності важливих заголовків
        assert 'content-type' in response['headers']
        assert 'application/json' in response['headers']['content-type']

    def test_api_performance(self):
        """Базовий тест продуктивності"""
        import time

        start_time = time.time()
        response = self.api.get("/posts")
        end_time = time.time()

        response_time = end_time - start_time

        # Перевірка, що відповідь приходить швидко (менше 2 секунд)
        assert response_time < 2.0, f"API відповідає занадто повільно: {response_time:.2f}s"
        assert response['status_code'] == 200
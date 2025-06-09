import json
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright


class BaseAPIController:
    """
    Базовий контролер для роботи з API.
    Надає основні методи для HTTP запитів та обробки відповідей.
    """

    def __init__(self, base_url: str, timeout: int = 30000):
        """
        Ініціалізація контролера

        Args:
            base_url: Базова URL для API
            timeout: Таймаут для запитів в мілісекундах
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.playwright = None
        self.request_context = None
        self.logger = logging.getLogger(__name__)

    def setup(self):
        """Налаштування Playwright та request context"""
        self.playwright = sync_playwright().start()
        self.request_context = self.playwright.request.new_context(
            base_url=self.base_url,
            timeout=self.timeout
        )

    def teardown(self):
        """Очищення ресурсів"""
        if self.request_context:
            self.request_context.dispose()
        if self.playwright:
            self.playwright.stop()

    def _build_url(self, endpoint: str) -> str:
        """Створення повної URL з endpoint"""
        return urljoin(f"{self.base_url}/", endpoint.lstrip('/'))

    def _prepare_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """Підготовка заголовків для запиту"""
        headers = self.default_headers.copy()
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def get(self, endpoint: str, params: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Виконання GET запиту

        Args:
            endpoint: API endpoint
            params: Query параметри
            headers: Додаткові заголовки

        Returns:
            Словник з даними відповіді
        """
        url = self._build_url(endpoint)
        prepared_headers = self._prepare_headers(headers)

        self.logger.info(f"GET запит до: {url}")

        response = self.request_context.get(
            url,
            params=params,
            headers=prepared_headers
        )

        return self._process_response(response)

    def post(self, endpoint: str, data: Optional[Dict] = None,
             headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Виконання POST запиту"""
        url = self._build_url(endpoint)
        prepared_headers = self._prepare_headers(headers)

        self.logger.info(f"POST запит до: {url}")

        response = self.request_context.post(
            url,
            data=json.dumps(data) if data else None,
            headers=prepared_headers
        )

        return self._process_response(response)

    def put(self, endpoint: str, data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Виконання PUT запиту"""
        url = self._build_url(endpoint)
        prepared_headers = self._prepare_headers(headers)

        self.logger.info(f"PUT запит до: {url}")

        response = self.request_context.put(
            url,
            data=json.dumps(data) if data else None,
            headers=prepared_headers
        )

        return self._process_response(response)

    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Виконання DELETE запиту"""
        url = self._build_url(endpoint)
        prepared_headers = self._prepare_headers(headers)

        self.logger.info(f"DELETE запит до: {url}")

        response = self.request_context.delete(
            url,
            headers=prepared_headers
        )

        return self._process_response(response)

    def _process_response(self, response) -> Dict[str, Any]:
        """
        Обробка відповіді від API

        Returns:
            Словник з статус кодом, заголовками та даними
        """
        result = {
            'status_code': response.status,
            'headers': dict(response.headers),
            'url': response.url
        }

        try:
            # Спроба парсингу JSON
            result['data'] = response.json()
        except:
            # Якщо не JSON, зберігаємо як текст
            result['data'] = response.text()

        self.logger.info(f"Отримано відповідь: {result['status_code']}")

        return result

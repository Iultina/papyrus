from abc import ABC
import httpx
from loguru import logger


class HTTPClient(ABC):
    """
    Отправляет асинхронный HTTP-запрос и возвращает результат в формате dict.

    Параметры:
        method (str): HTTP-метод (например, "GET", "POST", "PUT" и т.д.).
        endpoint (str): Полный URL-адрес или путь к API-методу.
        **options: Дополнительные параметры запроса, такие как headers, params, json и т.п.

    Возвращает:
        dict | None: Ответ сервера, если запрос успешен и ответ содержит JSON.
        В случае ошибки возвращает None и логирует её.

    Исключения:
        httpx.HTTPStatusError: При ответе с кодом ошибки (4xx/5xx).
        httpx.RequestError: При ошибках сети или DNS.
        Exception: При любых других ошибках.

    Примечание:
        Метод использует httpx.AsyncClient внутри контекста,
        поэтому соединение закрывается автоматически после запроса.
    """

    def __init__(self, base_url: str, timeout_seconds: int = 10) -> None:
        self._timeout = timeout_seconds
        self.base_url = base_url

    async def _send_request(self, method: str, endpoint: str, **options) -> dict | None:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as session:
                result = await session.request(method, endpoint, **options)
                result.raise_for_status()
                return await result.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP ошибка при доступе к {endpoint}: {exc}")
        except httpx.RequestError as exc:
            logger.error(f"Ошибка соединения при запросе к {endpoint}: {exc}")
        except Exception as exc:
            logger.error(f"Непредвиденная ошибка при запросе к {endpoint}: {exc}")

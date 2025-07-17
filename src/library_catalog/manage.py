import uvicorn
from app.infra.config import settings


def start():
    uvicorn.run(
        app="app.app:app",
        port=settings.port,
        host=settings.host,
        reload=True,
    )


if __name__ == "__main__":
    start()

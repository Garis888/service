import uvicorn

from src.config import settings
from src.app.app import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        access_log=True,
    )

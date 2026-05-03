from fastapi import FastAPI

from src.api import health, contact_routes
from src.conf.config import settings
from src.conf.constants import API_PREFIX

app = FastAPI(title="Contacts API")

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(contact_routes.router, prefix=API_PREFIX)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=int(settings.APP_PORT),
        reload=True,
    )


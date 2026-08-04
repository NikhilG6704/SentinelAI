from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

register_exception_handlers(app)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Log application startup information.
    """
    logger.info("%s Backend Started", settings.PROJECT_NAME)
    logger.info("Environment: %s", settings.ENVIRONMENT)
    logger.info("Version: %s", settings.VERSION)
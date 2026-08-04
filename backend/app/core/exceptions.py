"""
Global exception handlers.
"""

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("sentinelai")


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """
    Handle FastAPI HTTP exceptions.
    """
    logger.warning(
        "HTTP %s - %s (%s)",
        exc.status_code,
        exc.detail,
        request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
            },
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected exceptions.
    """
    logger.exception(
        "Unhandled exception on %s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal Server Error",
            },
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        global_exception_handler,
    )
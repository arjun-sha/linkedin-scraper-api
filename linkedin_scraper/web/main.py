import logging

from fastapi import FastAPI

from linkedin_scraper.web.routes import router


def main():
    """
    Initializes the web app
    Returns: Fast API App
    """
    uvicorn_logger = logging.getLogger("linkedin-scraper")
    uvicorn_logger.setLevel(logging.DEBUG)

    app = FastAPI()
    app.include_router(router)
    return app

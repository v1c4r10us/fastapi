from fastapi import FastAPI
from routes.user import user
from config.db import conn
from docs import tags_metadata

app = FastAPI(
    title="RestAPI with python",
    description="A simple API with fastapi & mongodb atlas",
    version="0.0.1",
    openapi_tags=tags_metadata
    )

app.include_router(user)
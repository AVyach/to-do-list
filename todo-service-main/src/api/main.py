from fastapi import FastAPI
from infrastructure.container import Container
from infrastructure.api.setup import setup
import uvicorn
import logging
import sys


def init():
    container = Container()
    app = FastAPI()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.extra["container"] = container
    setup(app, container)
    return app

app = init()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
    
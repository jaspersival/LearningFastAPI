from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


class UniCornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(UniCornException)
async def unicorn_exception_handler(request: Request, exc: UniCornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes rainbow..."},
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3")
    return {"item": item_id}


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UniCornException(name=name)
    return {"unicorn_name": name}

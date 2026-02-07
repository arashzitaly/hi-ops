import logging

from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hello_ops")

app = FastAPI(title="hello_ops")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        "%s %s -> %s",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/greet")
def greet(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

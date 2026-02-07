from fastapi import FastAPI

app = FastAPI(title="hello_ops")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}

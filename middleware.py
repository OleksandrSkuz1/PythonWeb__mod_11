from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response


app = FastAPI()

app.add_middleware(CustomHeaderMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}


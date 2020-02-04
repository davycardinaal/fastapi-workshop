from core.config import Settings
from database import SessionLocal
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response


app = FastAPI(title="fastapi-workshop")

# Set all CORS enabled origins
origins = []
if Settings().BACKEND_CORS_ORIGINS:
    origins_raw = Settings().BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(  # type: ignore
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  # Todo: not sure if we need cookie support
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Range"],
    ),


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}

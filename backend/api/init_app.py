from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def init_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from backend.api.v1 import router_v1
    app.include_router(router_v1, prefix="/api/v1")

    return app

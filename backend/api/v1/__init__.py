from fastapi import APIRouter
from .processamento.routes import router as processamento_router

router_v1 = APIRouter()

router_v1.include_router(processamento_router, prefix="/processamento", tags=["Processamento"])

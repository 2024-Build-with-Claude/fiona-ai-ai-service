import logging
import uuid

import firebase_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_profiler import PyInstrumentProfilerMiddleware
from firebase_admin import credentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config.logging_config import logger
from app.config.settings import settings
from app.controllers.v1.fiona_ai_chat_controller import fiona_ai_chat_controller
from app.controllers.v1.fiona_ai_proxy_controller import fiona_ai_proxy_controller
from app.controllers.v1.fiona_ai_resume_controller import fiona_ai_resume_controller
from app.infrastructure.apis import router as common_router
from app.user.apis import router as user_router

logging.getLogger().setLevel(logging.INFO)

app = FastAPI(title="AI Service", docs_url="/")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# profiler
if settings.PROFILING_ENABLED:
    app.add_middleware(
        middleware_class=PyInstrumentProfilerMiddleware,
    )

app.include_router(common_router, prefix="/internal/common", tags=["common"])
app.include_router(user_router, prefix="/user", tags=["user"])

############################################################################################
# Mufasa AI
############################################################################################

app.include_router(
    router=fiona_ai_resume_controller, prefix="/fiona_ai/v1/resume", tags=["resume"]
)

app.include_router(
    router=fiona_ai_chat_controller, prefix="/fiona_ai/v1/threads", tags=["chat"]
)

app.include_router(
    router=fiona_ai_proxy_controller, prefix="/fiona_ai/v1/proxy", tags=["proxy"]
)

############################################################################################


@app.on_event("startup")
async def startup_event():
    logger.critical("Application start")


@app.on_event("shutdown")
def shutdown_event():
    # scheduler.shutdown()
    logger.critical("Application shutdown")

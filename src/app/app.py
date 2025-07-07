from fastapi.middleware.cors import CORSMiddleware
from src.app.containers import container
from src.modules.service1.router import routers as monitoring_routers
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.core.rabbit import Rabbit
from contextlib import asynccontextmanager
from src.core.redis import Redis
from src.core.consts import HTTP_500_TEXT



@asynccontextmanager
async def lifespan(_: FastAPI):
    ret = await Rabbit().connect()
    if not ret:
        raise HTTPException(status_code=500, detail=HTTP_500_TEXT)
    yield
    await Rabbit().disconnect()
    
app = FastAPI(
    title='My App',
    container=container,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_routers():
    for router in monitoring_routers:
        app.include_router(
            router,
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": HTTP_500_TEXT,
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": HTTP_500_TEXT,
        },
    )

@app.exception_handler(HTTPException)
async def generic_exception_handler(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
        },
    )

init_routers()
if not Redis().init():
    raise HTTPException(status_code=500, detail=HTTP_500_TEXT)

import time

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Path
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException

from src.modules.service_a.schemas import CpeUpdate
from src.config import settings


SLEEP_SECONDS = 2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    time.sleep(SLEEP_SECONDS)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": 'Internal provisioning exception',
        },
    )

@app.exception_handler(Exception)
def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    time.sleep(SLEEP_SECONDS)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": 'Internal provisioning exception',
        },
    )

@app.exception_handler(HTTPException)
def generic_exception_handler(
    request: Request,
    exc: HTTPException,
):
    time.sleep(SLEEP_SECONDS)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
        },
    )

@app.post('/api/v1/equipment/cpe/{id}')
def set_configuration(
        inp: CpeUpdate,
        id: str = Path(..., pattern=r"^[a-zA-Z0-9]{6,}$")
):
    time.sleep(SLEEP_SECONDS)
    return JSONResponse(content={"message": "success"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        access_log=True,
    )
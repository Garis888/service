from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from src.core.containers import ContainerBuilder as cb
from ..gw.cpe_gw import CpeGW
from .. import schemas
from src.core.consts import Status
import json

router = APIRouter(
    prefix='/api/v1',
    tags=['CPE'],
)

@router.post(
    "/equipment/cpe/{id}",
    status_code=status.HTTP_200_OK,
)
@inject
async def update(
    inp: schemas.CpeUpdate,
    id: str = Path(..., regex=r"^[a-zA-Z0-9]{6,}$"),
    gw: CpeGW = Depends(Provide[cb().container.cpe.cpe_gw]),
):
    task_id = await gw.activate_cpe(id, inp)
    return  {
        "code": status.HTTP_200_OK,
        "taskId": task_id,
    }
    

@router.get(
    "/equipment/cpe/{id}/task/{task}",
    status_code=status.HTTP_200_OK,
)
@inject
async def read(
    task: str,
    id: str = Path(..., regex=r"^[a-zA-Z0-9]{6,}$"),
    gw: CpeGW = Depends(Provide[cb().container.cpe.cpe_gw]),
):
    code = None
    msg = ''
    success, st = await gw.read_cpe(id, task)
    if success:
        if not st:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested task is not found",
            )
        if st == Status.COMPLETE:
            code = status.HTTP_200_OK
            msg = "Completed"
        elif st == Status.RUNNING:
            code = status.HTTP_204_NO_CONTENT
            msg = "Task is still running"
        else:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal provisioning exception",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested equipment is not found",
        )
    return  {
        "code": code,
        "message": msg,
    }

@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
)
@inject
async def keys(
    gw: CpeGW = Depends(Provide[cb().container.cpe.cpe_gw]),
):
    code = None
    msg = ''
    keys = await gw.keys()
    return  {
        "keys": keys,
    }

@router.post(
    "/clear",
    status_code=status.HTTP_200_OK,
)
@inject
async def clear(
    gw: CpeGW = Depends(Provide[cb().container.cpe.cpe_gw]),
):
    await gw.clear()
    return {
        "code": status.HTTP_200_OK,
        "message": "success",
    }

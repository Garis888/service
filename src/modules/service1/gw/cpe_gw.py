
from src.core.base_gw import BaseGW
from .. import schemas
from src.core.redis import Redis
from src.core.rabbit import Rabbit
import uuid
import json
from datetime import datetime
from src.core.consts import Status, GLOBAL_QUEUE


class CpeGW(BaseGW):

    @classmethod
    async def clear(
        cls,
    ):
        await Redis().clear()
    
    @classmethod
    async def read_cpe(
        cls,
        id: str,
        task_id: str,
    ) -> str:
        status = Status.NONE
        current = await Redis().get_key(id)
        if not current:
            return False, status
        task = json.loads(current)
        task_status = task['status'] if task['id'] == task_id else None
        return True, task_status
    
    @classmethod
    async def keys(
        cls,
    ) -> str:
        keys = await Redis().keys()
        return keys
    
    @classmethod
    async def activate_cpe(
        cls,
        id: str,
        inp: schemas.CpeUpdate,
    ) -> str:
        current = await Redis().get_key(id)
        if current:
            task = json.loads(current)
            return task['id']
        timestamp = datetime.now().timestamp()
        p = inp.model_dump()
        task = {
            'timestamp': timestamp,
            'id': str(uuid.uuid4()),
            'equipment_id': id,
            'parameter': p,
            'status': Status.RUNNING,
        }
        task_dump = json.dumps(task).encode()
        await Redis().set_key(task['equipment_id'], task_dump)
        
        await Redis().rpush(GLOBAL_QUEUE, task['id'])
        
        await Rabbit().send_message(
            routing_key=task['id'],
            msg=task_dump,
        )
        
        return task['id']

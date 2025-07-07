from src.config import settings
import pika
import multiprocessing as mp
from src.core.redis_sync import Redis
from src.core.consts import GLOBAL_QUEUE
import time
import json
from src.core.consts import Status
from datetime import datetime
import requests
import traceback
from loguru import logger


class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None
        self._result = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return (self._exception)

def process_message(
        channel,
        method,
        properties,
        body,
        return_dict,
):
    print("Received message:", body)
    task = json.loads(body)
    equip_id = task.get('equipment_id')
    equip_par = task.get('parameter')
    responce = requests.post(f"{settings.SERVICE_A_URL}{equip_id}/", json=equip_par)
    if responce.status_code == 200:
        task_id = task['id']
        timestamp = datetime.now().timestamp()
        task['status'] = Status.COMPLETE
        task['timestamp'] = timestamp
        task_dump = json.dumps(task).encode()
        channel.basic_cancel(
            consumer_tag=channel.consumer_tags[0],
        )
        channel.basic_publish(
            exchange='',
            routing_key=task_id,
            body=task_dump,
        )
        return_dict[task_id] = task


def listen_to_queue(
        task_id: bytes,
        debug: bool,
        return_dict,
):
    queue_name = task_id

    with pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT_HOST)) as conn:
        channel = conn.channel()
        channel.queue_declare(
            queue=queue_name,
            exclusive=False,
            auto_delete=False,
        )
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=lambda ch, mt, pr, bd: process_message(ch, mt, pr, bd, return_dict),
            auto_ack=True,
        )
        channel.start_consuming()


if __name__ == "__main__":
    manager = mp.Manager()
    return_dict = manager.dict()
    debug = False
    if debug:
        settings.RABBIT_HOST = 'localhost'
        settings.REDIS_HOST = 'localhost'
    Redis().init()
    processes = []
    while True:
        try:
            task_id = (Redis().lpop(GLOBAL_QUEUE)).decode('utf-8')
        except Exception as ex:
            logger.error(f"Err: {ex}")
            Redis().init()
            task_id = None
        if not task_id:
            time.sleep(1)
            continue
        logger.info(f"Get task_id: {task_id} ")
        p = Process(
            target=listen_to_queue,
            args=(task_id, debug, return_dict),
        )
        processes.append(p)
        p.start()
        p.join()
        logger.info(f"Process for task_id: {task_id} join")

        if p.exception:
            error, traceback = p.exception
            logger.info(f"Process for task_id: {task_id} ")
            while True:
                try:
                    Redis().rpush(
                        redis_queue=GLOBAL_QUEUE,
                        val=task_id,
                    )
                    break
                except Exception as ex:
                    time.sleep(1)
                    continue
        elif task_id in return_dict:
            task = return_dict[task_id]
            task_dump = json.dumps(task)
            logger.info(f"Result: {return_dict[task_id]} ")
            Redis().set_key(task['equipment_id'], task_dump)

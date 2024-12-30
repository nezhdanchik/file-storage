import os
import time
import bz2

from celery import Celery
from settings import get_celery_broker_url

app = Celery('tasks', broker=get_celery_broker_url())

@app.task(name='write_file')
def write_file(incoming_bytes: bytes, filepath: str):
    print(f"Writing file to {filepath}")
    time.sleep(5)
    print("After sleep")
    with open(filepath, 'wb') as f:
        f.write(incoming_bytes)


@app.task(name='write_compressed_file')
def write_compressed_file(incoming_bytes: bytes, filepath: str):
    print(f"Writing file to {filepath}")
    with bz2.open(filepath, "wb") as fout:
        fout.write(incoming_bytes)
    print(f"File written to {filepath}")

@app.task(name='delete_file')
def delete_file(filepath: str):
    print(f"Deleting file {filepath}")
    os.remove(filepath)
    print(f"File {filepath} deleted")
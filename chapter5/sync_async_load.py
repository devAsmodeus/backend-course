import time
import uvicorn
import asyncio
import threading

from fastapi import FastAPI


app = FastAPI()


@app.get(path='/sync/{id_process}')
def sync_func(
        id_process: int
) -> None:
    print(f'Активных потоков: {threading.active_count()}')
    print(f'Запущен sync процесс: {id_process}')
    time.sleep(3)
    print(f'Завершен sync процесс: {id_process}')


@app.get(path='/async/{id_process}')
async def async_func(
        id_process: int
) -> None:
    print(f'Активных потоков: {threading.active_count()}')
    print(f'Запущен async процесс: {id_process}')
    await asyncio.sleep(3)
    print(f'Завершен async процесс: {id_process}')


if __name__ == '__main__':
    uvicorn.run(app='sync_async_load:app', reload=True)

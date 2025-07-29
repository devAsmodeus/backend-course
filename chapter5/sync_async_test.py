import asyncio
import aiohttp

from datetime import datetime


async def main() -> None:
    start_time = datetime.now()
    await asyncio.gather(*[
        parse('async', index) for index in range(1, 101)
    ])
    print(datetime.now() - start_time)


async def parse(
        method: str,
        process_id: int
) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'http://127.0.0.1:8000/{method}/{process_id}'
        ) as _:
            print(f'Закончил выполнение: {process_id}')


if __name__ == '__main__':
    asyncio.run(main())

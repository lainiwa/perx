import asyncio

from aiohttp import web
from perx.web import app
from perx.worker import consumer
from perx.config import settings

async def main():
    await asyncio.gather(
        web._run_app(app, port=8000),
        *[consumer(idx=i) for i in range(settings.workers_num)],
    )


loop = asyncio.get_event_loop()
asyncio.ensure_future(main())
loop.run_forever()
loop.close()

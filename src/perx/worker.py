import asyncio

from aiohttp import web

from perx import queue, results
from perx.models import Result


async def consumer():
    while True:
        # Wait until queue not empty
        if not queue:
            await asyncio.sleep(0.1)
            continue
        # Get element from queue
        head = queue.pop(0)
        # Continue if already started processing
        if isinstance(head, Result) and head.times_applied < head.n:
            head.current_val += head.d
            head.times_applied += 1
            queue.insert(0, head)
            await asyncio.sleep(head.interval)
        # If processing finished - move to `processed` list
        elif isinstance(head, Result) and head.times_applied == head.n:
            results.append(head)
        # If processing not yet started - convert `Task` to `Result`
        else:
            head = Result(**head.dict())
            queue.insert(0, head)


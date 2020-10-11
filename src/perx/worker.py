import asyncio

from aiohttp import web

from perx import queue, processed, results
from perx.models import Result


async def consumer(*, idx):
    while True:
        head = processed[idx]

        # If already processing a task
        if head:
            # If not yet finished - continue processing
            if head.times_applied < head.n:
                head.current_val += head.d
                head.times_applied += 1
                processed[idx] = head
                await asyncio.sleep(head.interval)
            # If finished - remove from `processed` to `results`
            if head.times_applied == head.n:
                results.append(head)
                processed[idx] =None

            continue

        # If no tasks being processed, but we can get task from queue
        # move from `queue` to `processed`
        if queue:
            head = queue.pop(0)
            head = Result(**head.dict())
            processed[idx] = head

            continue

        # Otherwise just wait until queue not empty
        await asyncio.sleep(0.1)

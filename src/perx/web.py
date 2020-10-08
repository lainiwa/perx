from aiohttp import web
from pydantic.error_wrappers import ValidationError
from perx import queue, results
from perx.models import Task, Result

routes = web.RouteTableDef()


@routes.post('/enqueue')
async def enqueue(request):
    try:
        task = Task(**request.rel_url.query)
        queue.append(task)
        return web.Response(text=f'{repr(task)} pushed into queue')

    except ValidationError:
        raise web.HTTPBadRequest(reason='Request arguments invalid.')


@routes.get('/peek')
async def peek(request):
    print('Results: ', results)

    resp = [{
        'n_in_queue': i,
        'status': 'active' if isinstance(task, Result) else 'waiting',
        'N': task.n,
        'D': task.d,
        'N1': task.n1,
        'interval': task.interval,
        'current_val': task.current_val if isinstance(task, Result) else None,
        'started': task.started.isoformat() if isinstance(task, Result) else None,
    } for i, task in enumerate(queue)]

    return web.json_response(resp)


app = web.Application()
app.add_routes(routes)

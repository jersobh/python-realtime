import asyncio
import json
from aiohttp.web import Application, Response
from aiohttp_sse import sse_response
import aiohttp_cors
import sockjs


score = {'cruzeiro': 0, 'atletico': 0}
ws = []


async def vote_cruzeiro(request):
    score['cruzeiro'] += 1
    for ws_session in ws:
        data = json.dumps(score)
        ws_session.manager.broadcast(data)
    return Response()


async def vote_atletico(request):
    score['atletico'] += 1
    for ws_session in ws:
        data = json.dumps(score)
        ws_session.manager.broadcast(data)
    return Response()


async def sse_poll(request):
    async with sse_response(request) as resp:
        while True:
            data = json.dumps(score)
            await resp.send(data)
            await asyncio.sleep(0.001)


async def ws_poll(msg, session):
    if msg.type == sockjs.MSG_OPEN:
        ws.append(session)
        for ws_session in ws:
            data = json.dumps(score)
            ws_session.manager.broadcast(data)
        print("Someone joined")
    elif msg.type == sockjs.MSG_MESSAGE:
        session.manager.broadcast(msg.data)
    elif msg.type == sockjs.MSG_CLOSED:
        ws.remove(session)
        print("Someone left.")


async def factory():
    loop = asyncio.get_event_loop()
    app = Application(loop=loop)
    app['channels'] = set()

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    cors.add(app.router.add_route('POST', '/vote_cruzeiro', vote_cruzeiro))
    cors.add(app.router.add_route('POST', '/vote_atletico', vote_atletico))
    cors.add(app.router.add_route('GET', '/sse/', sse_poll))
    sockjs.add_endpoint(app, ws_poll, name='ws', prefix='/ws/')
    return app

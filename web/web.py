import sys

sys.path.append("..")

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute
from peewee import *
from playhouse.shortcuts import model_to_dict

from db.models import User, Recommendation

db = PostgresqlDatabase('computeinsight', user='postgres', password='computeinsight', host='localhost', port=5432)


def user_recommendations(request):
    username = request.path_params['username']

    with db:
        recommendations = Recommendation.select(Recommendation.track_title,
                                                Recommendation.track_id,
                                                Recommendation.track_link, ) \
            .join(User) \
            .where(User.username == username)

    return JSONResponse([model_to_dict(item) for item in recommendations])


async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text('Hello, websocket!')
    await websocket.close()


def startup():
    pass


routes = [
    Route('/user-recommendations/{username}', user_recommendations),
    WebSocketRoute('/ws', websocket_endpoint),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])

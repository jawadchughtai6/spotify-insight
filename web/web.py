import sys
import datetime

sys.path.append("..")

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from peewee import *
from playhouse.shortcuts import model_to_dict

from db.models import User, Recommendation
from application import Application

app = Application('Compute Insight')

db = PostgresqlDatabase(app.env('DB'),
                        user=app.env('DB_USER'),
                        password=app.env('DB_PASSWORD'),
                        host=app.env('DB_HOST'),
                        port=app.env('DB_PORT'))


def user_recommendations(request):
    username = request.path_params['username']
    date = request.query_params['date'] if 'date' in request.query_params else None

    if date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        date = datetime.datetime.now().date()

    with db:
        recommendations = Recommendation.select(Recommendation.id,
                                                Recommendation.track_title,
                                                Recommendation.track_id,
                                                Recommendation.track_link,
                                                Recommendation.user) \
            .join(User) \
            .where((User.username == username) &
                   (fn.date_trunc('day', Recommendation.created_at) == date))

    return JSONResponse([model_to_dict(item) for item in recommendations])


routes = [
    Route('/user-recommendations/{username}', user_recommendations),
]

app = Starlette(debug=True, routes=routes)

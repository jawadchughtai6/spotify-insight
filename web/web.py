import datetime
import sys
from peewee import fn
from playhouse.shortcuts import model_to_dict
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from application import Application
from db.models import User, Recommendation

config = Application("Compute Insight")


def user_recommendations(request):
    """
    Get request for fetching spotify recommendations against provided username and
    the date for which information is required.
    """
    username = request.path_params["username"]
    date = request.query_params["date"] if "date" in request.query_params else None

    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d") if date else datetime.datetime.now().date()
    except ValueError as ve:
        return JSONResponse({"Error": "Kindly provide valid date format"})

    with config.db_session("recommendations"):
        recommendations = (
            Recommendation.select(
                Recommendation.id,
                Recommendation.track_title,
                Recommendation.track_id,
                Recommendation.track_link,
                Recommendation.user
            )
            .join(User)
            .where(
                (User.username == username)
                & (fn.date_trunc("day", Recommendation.created_at) == date)
            )
        )

    return JSONResponse([model_to_dict(item) for item in recommendations])


routes = [
    Route("/user-recommendations/{username}", user_recommendations),
]

app = Starlette(debug=True, routes=routes)

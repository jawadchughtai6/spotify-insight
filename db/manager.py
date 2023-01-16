from db.models import User, Recommendation


class Manager:
    """
    Base singleton manager class for connecting and interacting with database.
    """
    _instance = None

    def __init__(self, app):
        self.app = app
        self.create_tables()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def create_tables(self):
        """
        Create required tables in connected database for relevant scope.
        """
        with self.app.db_session("recommendations") as db:
            db.create_tables([User, Recommendation])

    def create_recommendations(self, username, recommended_tracks):
        """
        Add user related recommended tracks to the database.

        param str username: username against which recommended songs are to be stored.
        param list[dict] recommended_tracks: tracks
        """
        with self.app.db_session("recommendations") as db:
            user, created = User.get_or_create(
                username=username,
                defaults={
                   "client_id": self.app.env("CLIENT_ID"),
                   "client_secret": self.app.env("CLIENT_SECRET")
                }
            )
            tracks_to_create = [
                {
                    "user": user,
                    "track_id": track["id"],
                    "track_title": track["name"],
                    "track_link": track["uri"],
                }
                for track in recommended_tracks
            ]

            with db.atomic():
                Recommendation.insert_many(tracks_to_create).execute()

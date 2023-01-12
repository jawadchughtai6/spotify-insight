from db.models import User, Recommendation


class Manager:

    def __init__(self, app):
        self.app = app
        self.create_tables()

    def create_tables(self):
        with self.app.db_session('recommendations') as db:
            db.create_tables([User, Recommendation])

    def create_recommendations(self, username, recommended_tracks):
        with self.app.db_session('recommendations') as db:
            user, created = User.get_or_create(username=username,
                                               defaults={'client_id': self.app.env('CLIENT_ID'),
                                                         'client_secret': self.app.env('CLIENT_SECRET')})
            tracks_to_create = []
            for track in recommended_tracks:
                tracks_to_create.append({
                    "user": user,
                    "track_id": track['id'],
                    "track_title": track["name"],
                    "track_link": track["uri"],
                })

            with db.atomic():
                Recommendation.insert_many(tracks_to_create).execute()

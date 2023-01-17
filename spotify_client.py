import requests

from application import Application
from db.manager import Manager


class SpotifyClient:
    """
    Bridge for interacting with Spotify Application. Establishes connection with Spotify in order to retrieve
    music recommendations of desired user.
    """

    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager
        self.client_id = app.env("CLIENT_ID", "")
        self.client_secret = app.env("CLIENT_SECRET", "")
        self.seed_artist = app.env("SEED_ARTIST")
        self.seed_genres = app.env("SEED_GENRES")
        self.seed_tracks = app.env("SEED_TRACKS")
        self.base_url = app.env("BASE_URL", "https://api.spotify.com/v1")
        self.authorization_url = app.env("SPOTIFY_AUTHORIZATION_URL", "https://accounts.spotify.com/api/token")

    def request_authorization(self):
        """
        Makes authorization request to Spotify application in order to
        retrieve access token required for further interaction.

        return str: Access token for authorized user.
        """

        response = requests.post(
            self.authorization_url,
            {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )

        auth_response_data = response.json()
        return auth_response_data["access_token"]

    def get_recommendations(self, access_token):
        """
        Fetches list of recommendation from spotify api client against authorized user.

        param str access_token: Access token for authorized user.
        return list[dict]: Recommended tracks for provided user.
        """
        url = f"{self.base_url}/recommendations"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        params = {
            "seed_artists": self.seed_artist,
            "seed_genres": self.seed_genres,
            "seed_tracks": self.seed_tracks,
        }

        response = requests.get(url, headers=headers, params=params)
        tracks = response.json()["tracks"]

        return tracks

    def call(self):
        """
        Main driver for invoking Spotify client. Fetches recommendations and stores them in database.
        """
        access_token = self.request_authorization()
        recommended_tracks = self.get_recommendations(access_token)
        self.db_manager.create_recommendations(self.app.env("USERNAME", ""), recommended_tracks)


if __name__ == "__main__":
    app = Application("Compute Insight")
    db_manager = Manager(app)
    app.run(SpotifyClient(app, db_manager).call)

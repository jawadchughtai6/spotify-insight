import requests

from application import Application
from db.manager import Manager


class SpotifyClient:
    """
    Interaction with the Spotify Web API
    """

    def __init__(self, app, db_manager):
        #  TODO: These are to be loaded from environment or database
        self.app = app
        self.db_manager = db_manager
        self.client_id = app.env('CLIENT_ID', '')
        self.client_secret = app.env('CLIENT_SECRET', '')
        self.base_url = app.env('BASE_URL', 'https://api.spotify.com/v1')

    def request_authorization(self):
        authorization_url = 'https://accounts.spotify.com/api/token'

        response = requests.post(authorization_url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })

        auth_response_data = response.json()
        return auth_response_data['access_token']

    def get_recommendations(self, access_token):
        url = self.base_url + '/recommendations'

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }

        params = {
            "seed_artists": "4NHQUGzhtTLFvgF5SZesLK",
            "seed_genres": "classical,country",
            "seed_tracks": "0c6xIDDpzE81m2q797ordA"
        }

        response = requests.get(url, headers=headers, params=params)
        tracks = response.json()['tracks']
        return tracks

    def call(self):
        access_token = self.request_authorization()
        recommended_tracks = self.get_recommendations(access_token)
        self.db_manager.create_recommendations(self.app.env('USERNAME', ''), recommended_tracks)


if __name__ == '__main__':
    app = Application('Compute Insight')
    db_manager = Manager(app)
    app.run(SpotifyClient(app, db_manager).call)

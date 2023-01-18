# Spotify Insight
This application communicates with the Spotify Web API to fetch track recommendations against the provided user.

## Tech Stack
- Python 3.10
- [Starlette](https://www.starlette.io/)
- [Peewee](https://docs.peewee-orm.com/en/latest/)
- [Uvicorn](https://www.uvicorn.org/) 
- PostgreSQL
- Docker

## Directory Structure
```
spotify-insight
└───db  # Database related code goes here 
│   │   manager.py
│   │   models.py
│   
└───web # Web API's on Starlette go here    
│   │   Dockerfile.dev
│   │   web.py
│   
│   application.py    # App configurations exist here 
│   spotify_client.py # Communicates with the Spotify Web API  
│   docker-compose.dev.yml   
│   Dockerfile.dev   
│   .env.development   
│   Pipfile  
│   Pipfile.lock   
│   cron.sh   
│   spotify.cronjob   
│   README.md   

```

## Setting up local environment

### Pre-requisites
- Docker
- docker-compose
- You have created a Spotify app following the [app settings guide](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/).

### Update .env.development
Using the credentials obtained from the Spotify app, and the desired seeds, update the following in .env.development
- `CLIENT_ID`
- `CLIENT_SECRET`
- `USERNAME`

The `USERNAME` can be any alias name against the above credentials. Add them as per wish.

Recommendations are generated based on the available information for a given seed entity and matched against similar 
artists and tracks. If there is sufficient information about the provided seeds, a list of tracks will be returned. 
Please note that a default set of values have been set in the environment so updating the following is optional. 
For more information, use [this](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recommendations) 
as a guide.
- `SEED_ARTIST`
- `SEED_GENRES`
- `SEED_TRACKS`


### Running the containers
- `docker-compose -f docker-compose.dev.yml up --build`

### Initial database dump
#### In a new terminal:
- `docker-compose -f docker-compose.dev.yml exec app bash`
- `python3 spotify_client.py`

You should now have your database populated.

### Web API
The following API returns recommendations for the given user on a given date:

`http://0.0.0.0:8000/user-recommendations/{username}?date={yyyy-mm-dd}`

## Installing a new package
- `docker-compose -f docker-compose.dev.yml exec app bash`
- `pipenv install {Package Name}`

## Approach
Recommendations of the given user are fetched after using 
[client credentials flow](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/) for authentication.
At the moment, we are fetching data only for the given user (.env.development) 
but this can be expanded to retrieve recommendations for different users dynamically.

There are three docker containers set up; One running PostgreSQL database, Second running a CRON Job scheduled for midnight, 
retrieving recommendations against given user every night and 
last running Starlette and Uvicorn for serving the Web API.
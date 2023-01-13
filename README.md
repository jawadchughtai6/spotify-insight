# Spotify Insight

## Setting up local environment

### Pre-requisites
- Docker
- Pipenv

### Install dependencies
- `pipenv install`

### Run PostgreSQL on Docker and set up a database
- `docker run -d -p 5432:5432 --name computeinsight -e POSTGRES_PASSWORD=computeinsight postgres`

#### In a new terminal:
- `docker exec -it computeinsight bash`
- `psql -U postgres`
- `CREATE DATABASE computeinsight`

### Update .env.development
- `Update CLIENT_ID`
- `Update CLIENT_SECRET`
- `Update USERNAME`

### Running Spotify Client
`python3 spotify_client.py`

### Running Starlette
#### In a new terminal
- `cd web`
- `uvicorn web:app`
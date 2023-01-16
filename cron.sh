#!/bin/bash
cd /code
PATH=/usr/local/bin:$PATH
/usr/local/bin/pipenv install
/usr/local/bin/pipenv run python -m spotify_client

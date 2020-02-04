# fastapi-workshop

This is the fastapi version of the workshop

## Install

```
mkvirtualenv --python=/usr/local/bin/python3 fastapi-workshop
pip install -r requirements.txt
createdb workskop
createuser workshop -sP
psql -d workshop < workshop_initial.psql
uvicorn main:app --reload
```
## Other commands and URL's:

```
http://127.0.0.1:8000/docs
```

or

```
http://127.0.0.1:8000/redoc
```

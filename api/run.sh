#!/bin/bash

[ -d env ] || (
  python -m venv env
  . env/bin/activate
  pip install -r requirements.txt
)

[ -d ../dist ] || (
  cd ..
  [ -d node_modules ] || npm i
  npm run build
)

[ -f .env ] || (
  cp .env.example .env
  echo FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex())')" >> .env
)

[ -f sqlite.db ] || (
  . env/bin/activate
  export $(xargs <.env)
  ./seed.py
)

. env/bin/activate
flask --debug run

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

. env/bin/activate
flask --debug run

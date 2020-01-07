#!/bin/bash

uwsgi -y uwsgi.yaml:app &
UWSGI_PID=$!

cd elm
echo "start"

elm-live -d ../static -x /schedule -y http://localhost:9000/schedule src/Main.elm -- --debug --output=../static/main.js &

ELM_PID=$!
trap 'trap - SIGINT SIGTERM ERR; kill $ELM_PID;' SIGINT SIGTERM ERR

wait $ELM_PID

echo "killing"

kill $UWSGI_PID

wait $UWSGI_PID

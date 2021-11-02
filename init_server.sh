#!/usr/bin/bash
source ./socket/bin/activate

gunicorn --bind=0.0.0.0 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --threads 100 app:app


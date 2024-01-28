#!/bin/bash

use_redis_docker=$1

if [[ $use_redis_docker = "--redis-docker" ]]; then
  docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
fi
gunicorn --bind 0:8000 -w 4 -t 2 -k uvicorn.workers.UvicornWorker main:app
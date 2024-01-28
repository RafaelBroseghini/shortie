# shortie

> A FastAPI + Redis URL Shortener :)

## Prerequisites

`shortie` requires a running instance of Redis version >=6, either locally or hosted.

## How to start

> The `start.sh` script provides a helper flag to run a local `redis-stack-server` container.

```bash
./start.sh --redis-docker
```

If you'd like to point your app to a different redis instance, omit the `--redis-docker` and check [config.py](./app/core/config.py) to see what variables can be overriden.

Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to see the api docs.

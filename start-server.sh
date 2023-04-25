#!/bin/bash
gunicorn --bind 0:8000 -w 4 -t 2 -k uvicorn.workers.UvicornWorker main:app
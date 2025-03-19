# flake8: noqa

import os

bind = "0.0.0.0:5000"
workers = os.environ.get("gunicorn_workers", 2)
threads = os.environ.get("gunicorn_threads", 2)
worker_class = "uvicorn.workers.UvicornWorker"
log_config = None

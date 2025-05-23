#!/usr/bin/env python
"""Create Nginx/Gunicorn entrypoint for Sagemaker async."""
# This file implements the scoring service shell. You don't necessarily need to modify it for various
# algorithms. It starts nginx and gunicorn with the correct configurations and then simply waits until
# gunicorn exits.
#
# The flask server is specified to be the app object in wsgi.py
#
# We set the following parameters:
#
# Parameter                Environment Variable              Default Value
# ---------                --------------------              -------------
# number of workers        MODEL_SERVER_WORKERS              the number of CPU cores
# timeout                  MODEL_SERVER_TIMEOUT              60 seconds

import os
import signal
import subprocess
import sys
from uvicorn.workers import UvicornWorker

cpu_count = os.cpu_count() or 1

model_server_timeout = 3600
model_server_workers = int(cpu_count)


def sigterm_handler(nginx_pid: int, gunicorn_pid: int) -> None:
    """Kill nginx and gunicorn processes using SIGTERM.

    Parameters
    ----------
    nginx_pid : int
        process id of nginx
    gunicorn_pid : int
        process id of gunicorn
    """
    try:
        os.kill(nginx_pid, signal.SIGQUIT)
    except OSError:
        pass
    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    sys.exit(0)


def start_server() -> None:
    """Start checkbox_detector Extractor's Nginx/Gunicorn server."""
    print(f"Starting the inference server with {model_server_workers} workers.")

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(["ln", "-sf", "/dev/stdout", "/var/log/nginx/access.log"])
    subprocess.check_call(["ln", "-sf", "/dev/stderr", "/var/log/nginx/error.log"])

    nginx = subprocess.Popen(["nginx", "-c", "/opt/program/src/nginx.conf"])
    gunicorn = subprocess.Popen(
        [
            "gunicorn",
            "--timeout",
            str(model_server_timeout),
            "-k",
            "uvicorn.workers.UvicornWorker",
            "--bind",
            "unix:/tmp/gunicorn.sock",  # Update the socket path
            "src.app.app:app",
        ]
    )

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))

    # If either subprocess exits, so do we.
    pids = {nginx.pid, gunicorn.pid}
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)
    print("Inference server exiting")


# The main routine just invokes the start function.
if __name__ == "__main__":
    start_server()

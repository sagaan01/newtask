"""PyTest fixtures: auto-start the app under test, provide an API client."""

import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

APP_SERVER = Path(__file__).resolve().parent.parent / "app" / "server.py"
PORT = 8788


@pytest.fixture(scope="session")
def base_url():
    proc = subprocess.Popen(
        [sys.executable, str(APP_SERVER), "--port", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://localhost:{PORT}"
    for _ in range(50):
        try:
            if requests.get(f"{url}/health", timeout=1).status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(0.1)
    else:
        proc.terminate()
        pytest.fail("App under test did not start")

    yield url
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture
def api(base_url):
    session = requests.Session()
    session.base_url = base_url
    return session

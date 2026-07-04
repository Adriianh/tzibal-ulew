"""
Application entry point — launches API server and UI.
"""

from __future__ import annotations

import sys
import time

import httpx
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication

from config import API_HOST, API_PORT
from ui.app import MainWindow


def _wait_for_api(timeout: int = 10) -> bool:
    """Poll /health until the API responds or timeout expires."""
    url = f"http://{API_HOST}:{API_PORT}/health"
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = httpx.get(url)
            if resp.status_code == 200:
                return True
        except httpx.RequestError:
            pass
        time.sleep(0.2)
    return False


def main() -> int:
    app = QApplication(sys.argv)

    # 1. Start the API server
    api_process = QProcess()
    api_process.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
    api_process.start("uvicorn", ["api.main:app", "--host", API_HOST, "--port", str(API_PORT)])

    # 2. Wait for it to be ready
    if not _wait_for_api():
        print("Error: API did not start in time")
        return 1

    # 3. Launch the UI
    window = MainWindow()
    window.show()

    # 4. Clean shutdown when the app is closed
    def shutdown() -> None:
        try:
            httpx.post(f"http://{API_HOST}:{API_PORT}/shutdown", timeout=2)
        except Exception:
            pass
        api_process.waitForFinished(3000)
        api_process.kill()

    app.aboutToQuit.connect(shutdown)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

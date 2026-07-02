"""
Internal endpoints for system management (UI→API communication).
"""

import os
import signal

from fastapi import APIRouter, status

router = APIRouter(tags=["System"])


@router.post("/shutdown", status_code=status.HTTP_204_NO_CONTENT)
def shutdown() -> None:
    """Gracefully shuts down the API server.

    Called by the PyQt6 UI when the application closes.
    Sends SIGINT to the current process; Uvicorn handles cleanup.
    """
    os.kill(os.getpid(), signal.SIGINT)

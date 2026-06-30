"""
Centralized configuration file for the application.
Everything is defined in one place to make it easier to manage and change settings as needed.
"""

from pathlib import Path

# ── Base directories ──────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"
DB_DIR = PROJECT_ROOT

# ── Database ─────────────────────────────────────────────
DB_NAME = "tzibal_ulew.db"
DB_URL = f"sqlite:///{DB_DIR / DB_NAME}"

# ── API ───────────────────────────────────────────────────────
API_HOST = "127.0.0.1"
API_PORT = 8000
API_URL = f"http://{API_HOST}:{API_PORT}"

# ── Logging ───────────────────────────────────────────────────
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

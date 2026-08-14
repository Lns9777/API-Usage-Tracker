from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "backend" / "app" / "static" / "index.html"
ASSETS = ROOT / "backend" / "app" / "static" / "assets"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("frontend assets are missing from backend/app/static. Run package_frontend_assets.py first.")
    if not ASSETS.exists():
        raise SystemExit("frontend assets folder is missing from backend/app/static/assets.")
    print("Frontend assets are present.")


if __name__ == "__main__":
    main()

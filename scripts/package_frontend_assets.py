from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "frontend" / "dist"
TARGET = ROOT / "backend" / "app" / "static"


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit("frontend/dist does not exist. Run `cd frontend && npm run build` first.")

    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET)
    print(f"Copied frontend build from {SOURCE} to {TARGET}")


if __name__ == "__main__":
    main()

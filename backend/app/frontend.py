from __future__ import annotations


from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .paths import get_frontend_dist_dir


def mount_frontend(app, prefix: str = "") -> None:
    static_dir = get_frontend_dist_dir()
    if static_dir.exists():
        app.mount(
            prefix or "/assets",
            StaticFiles(directory=static_dir / "assets"),
            name="assets",
        )


def register_frontend_routes(router: APIRouter) -> None:
    static_dir = get_frontend_dist_dir()
    index_path = static_dir / "index.html"

    if not index_path.exists():
        return

    @router.get("/{path:path}")
    @router.get("/")
    def serve_frontend(path: str = ""):
        target = static_dir / path
        if path and target.exists() and target.is_file():
            return FileResponse(target)
        return FileResponse(index_path)

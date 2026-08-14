from backend.app import paths


def test_database_path_uses_explicit_overrides(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"
    db_path = tmp_path / "custom" / "tracker.db"

    monkeypatch.setenv("API_TRACKER_DATA_DIR", str(data_dir))
    monkeypatch.delenv("API_TRACKER_DB_PATH", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    assert paths.get_data_dir() == data_dir
    assert paths.get_database_path() == data_dir / "api_tracker.db"
    assert (
        paths.get_database_url()
        == f"sqlite:///{(data_dir / 'api_tracker.db').as_posix()}"
    )

    monkeypatch.setenv("API_TRACKER_DB_PATH", str(db_path))
    assert paths.get_database_path() == db_path

    monkeypatch.setenv("DATABASE_URL", "sqlite:///./override.db")
    assert paths.get_database_url() == "sqlite:///./override.db"

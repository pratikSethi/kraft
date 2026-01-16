"""Tests for add-on manager."""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from kraft.addon_manager import AddOnManager
from kraft.cli import app

runner = CliRunner()


class TestAddOnManager:
    """Tests for AddOnManager class."""

    def test_list_addons(self) -> None:
        manager = AddOnManager()
        addons = manager.list_addons()
        assert len(addons) >= 1
        assert any(a["name"] == "postgres" for a in addons)

    def test_get_addon_info_postgres(self) -> None:
        manager = AddOnManager()
        info = manager.get_addon_info("postgres")
        assert info is not None
        assert info["name"] == "postgres"
        assert "dependencies" in info

    def test_get_addon_info_nonexistent(self) -> None:
        manager = AddOnManager()
        info = manager.get_addon_info("nonexistent")
        assert info is None


class TestAddonsCommand:
    """Tests for addons command."""

    def test_addons_shows_list(self) -> None:
        result = runner.invoke(app, ["addons"])
        assert result.exit_code == 0
        assert "postgres" in result.output.lower()


class TestAddCommand:
    """Tests for add command."""

    def test_add_requires_kraft_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(app, ["add", "postgres", "--dir", tmpdir])
            assert result.exit_code == 1
            assert "not a kraft" in result.output.lower()

    def test_add_postgres_to_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # First create a project
            result = runner.invoke(
                app, ["create", "test-api", "--output", tmpdir + "/test-api"]
            )
            assert result.exit_code == 0

            # Then add postgres
            result = runner.invoke(
                app, ["add", "postgres", "--dir", tmpdir + "/test-api"]
            )
            assert result.exit_code == 0

            # Verify files were created
            project_dir = Path(tmpdir) / "test-api"
            assert (project_dir / "src" / "test_api" / "database.py").exists()
            assert (project_dir / "src" / "test_api" / "models_db.py").exists()

            # Verify .kraft.yml was updated
            import yaml

            with open(project_dir / ".kraft.yml") as f:
                config = yaml.safe_load(f)
            assert "postgres" in config.get("addons", [])

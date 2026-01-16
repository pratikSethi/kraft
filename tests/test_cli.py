"""Tests for CLI commands."""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from kraft.cli import app

runner = CliRunner()


class TestVersionCommand:
    """Tests for version command."""

    def test_version_displays(self) -> None:
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "kraft" in result.output
        assert "version" in result.output


class TestListCommand:
    """Tests for list command."""

    def test_list_shows_templates(self) -> None:
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "rest" in result.output.lower()


class TestCreateCommand:
    """Tests for create command."""

    def test_create_invalid_name_rejected(self) -> None:
        result = runner.invoke(app, ["create", "123invalid"])
        assert result.exit_code == 1
        assert "number" in result.output.lower()

    def test_create_rest_service(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                app, ["create", "test-api", "--output", tmpdir + "/test-api"]
            )
            assert result.exit_code == 0

            # Check files were created
            project_dir = Path(tmpdir) / "test-api"
            assert project_dir.exists()
            assert (project_dir / "pyproject.toml").exists()
            assert (project_dir / "README.md").exists()
            assert (project_dir / "Dockerfile").exists()
            assert (project_dir / "docker-compose.yml").exists()
            assert (project_dir / "src" / "test_api" / "main.py").exists()
            assert (project_dir / "src" / "test_api" / "routes.py").exists()
            assert (project_dir / "src" / "test_api" / "models.py").exists()

"""Add-on manager for kraft projects."""

from pathlib import Path

import yaml
from jinja2 import Template


class AddOnManager:
    """Manages add-on discovery and application."""

    def __init__(self) -> None:
        self.addons_dir = Path(__file__).parent / "addons"

    def list_addons(self) -> list[dict[str, str]]:
        """List all available add-ons."""
        addons = []
        for addon_dir in self.addons_dir.iterdir():
            if addon_dir.is_dir() and (addon_dir / "addon.yml").exists():
                info = self.get_addon_info(addon_dir.name)
                if info:
                    addons.append(info)
        return addons

    def get_addon_info(self, addon_name: str) -> dict | None:
        """Get metadata for an add-on."""
        addon_path = self.addons_dir / addon_name / "addon.yml"
        if not addon_path.exists():
            return None

        with open(addon_path) as f:
            config = yaml.safe_load(f)

        return {
            "name": config.get("name", addon_name),
            "description": config.get("description", ""),
            "version": config.get("version", "1.0.0"),
            "dependencies": config.get("dependencies", []),
        }

    def apply_addon(self, addon_name: str, project_dir: Path) -> None:
        """Apply an add-on to a kraft project."""
        # Validate project is a kraft project
        kraft_file = project_dir / ".kraft.yml"
        if not kraft_file.exists():
            raise ValueError(f"'{project_dir}' is not a kraft project (missing .kraft.yml)")

        # Load add-on config
        addon_path = self.addons_dir / addon_name / "addon.yml"
        if not addon_path.exists():
            raise ValueError(f"Add-on '{addon_name}' not found")

        with open(addon_path) as f:
            addon_config = yaml.safe_load(f)

        # Load project config
        with open(kraft_file) as f:
            project_config = yaml.safe_load(f)

        package_name = project_config.get("project", {}).get("package_name", "app")
        variables = {"package_name": package_name}

        # Update pyproject.toml with dependencies
        self._update_dependencies(project_dir, addon_config.get("dependencies", []))

        # Update docker-compose.yml with services
        if "docker_services" in addon_config:
            self._update_docker_compose(
                project_dir,
                addon_config.get("docker_services", {}),
                addon_config.get("docker_volumes", {}),
            )

        # Generate code files
        self._generate_addon_files(addon_name, project_dir, variables)

        # Update .env.example with new env vars
        if "env_vars" in addon_config:
            self._update_env_example(project_dir, addon_config["env_vars"])

        # Update README with add-on documentation
        self._update_readme(addon_name, project_dir, variables)

        # Update .kraft.yml with add-on metadata
        self._update_kraft_config(project_dir, addon_name)

    def _update_dependencies(self, project_dir: Path, dependencies: list[str]) -> None:
        """Add dependencies to pyproject.toml."""
        pyproject_path = project_dir / "pyproject.toml"
        if not pyproject_path.exists():
            return

        content = pyproject_path.read_text()

        # Find the dependencies section and add new deps
        for dep in dependencies:
            if dep not in content:
                # Find the closing bracket of dependencies
                import re

                pattern = r'(dependencies\s*=\s*\[[\s\S]*?)(])'
                match = re.search(pattern, content)
                if match:
                    deps_section = match.group(1)
                    # Add the new dependency before the closing bracket
                    new_deps = deps_section.rstrip() + f'\n    "{dep}",\n'
                    content = content[:match.start()] + new_deps + "]" + content[match.end():]

        pyproject_path.write_text(content)

    def _update_docker_compose(
        self, project_dir: Path, services: dict, volumes: dict
    ) -> None:
        """Update docker-compose.yml with new services."""
        compose_path = project_dir / "docker-compose.yml"
        if not compose_path.exists():
            return

        with open(compose_path) as f:
            compose = yaml.safe_load(f)

        # Add services
        if "services" not in compose:
            compose["services"] = {}
        compose["services"].update(services)

        # Add volumes
        if volumes:
            if "volumes" not in compose:
                compose["volumes"] = {}
            compose["volumes"].update(volumes)

        with open(compose_path, "w") as f:
            yaml.dump(compose, f, default_flow_style=False, sort_keys=False)

    def _generate_addon_files(
        self, addon_name: str, project_dir: Path, variables: dict
    ) -> None:
        """Generate code files from add-on templates."""
        addon_dir = self.addons_dir / addon_name
        src_dir = project_dir / "src" / variables["package_name"]
        src_dir.mkdir(parents=True, exist_ok=True)

        for template_file in addon_dir.glob("*.jinja"):
            if template_file.name == "readme-section.md.jinja":
                continue  # Handle separately

            content = template_file.read_text()
            template = Template(content)
            rendered = template.render(**variables)

            # Remove .jinja extension
            output_name = template_file.stem
            output_path = src_dir / output_name
            output_path.write_text(rendered)

    def _update_env_example(self, project_dir: Path, env_vars: dict) -> None:
        """Update .env.example with new environment variables."""
        env_path = project_dir / ".env.example"
        content = env_path.read_text() if env_path.exists() else ""

        for key, value in env_vars.items():
            if key not in content:
                content += f"\n{key}={value}"

        env_path.write_text(content.strip() + "\n")

    def _update_readme(
        self, addon_name: str, project_dir: Path, variables: dict
    ) -> None:
        """Append add-on documentation to README."""
        readme_section_path = self.addons_dir / addon_name / "readme-section.md.jinja"
        if not readme_section_path.exists():
            return

        readme_path = project_dir / "README.md"
        if not readme_path.exists():
            return

        content = readme_section_path.read_text()
        template = Template(content)
        rendered = template.render(**variables)

        readme_content = readme_path.read_text()
        readme_content += "\n" + rendered
        readme_path.write_text(readme_content)

    def _update_kraft_config(self, project_dir: Path, addon_name: str) -> None:
        """Update .kraft.yml with applied add-on."""
        kraft_path = project_dir / ".kraft.yml"
        with open(kraft_path) as f:
            config = yaml.safe_load(f)

        if "addons" not in config:
            config["addons"] = []

        if addon_name not in config["addons"]:
            config["addons"].append(addon_name)

        with open(kraft_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

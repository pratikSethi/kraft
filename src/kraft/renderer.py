"""Template rendering engine for kraft."""

import shutil
from datetime import datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    """Renders project templates using Jinja2."""

    def __init__(self) -> None:
        self.templates_dir = Path(__file__).parent / "templates"

    def list_templates(self) -> list[dict[str, str]]:
        """List all available templates."""
        templates = []
        for template_dir in self.templates_dir.iterdir():
            if template_dir.is_dir():
                info = self.get_template_info(template_dir.name)
                if info:
                    templates.append(info)
        return templates

    def get_template_info(self, template_name: str) -> dict[str, str] | None:
        """Get metadata for a template."""
        template_path = self.templates_dir / template_name / "template.yml"
        if not template_path.exists():
            return None

        with open(template_path) as f:
            config = yaml.safe_load(f)

        return {
            "name": config.get("name", template_name),
            "description": config.get("description", ""),
            "version": config.get("version", "1.0.0"),
        }

    def render(
        self,
        template_name: str,
        output_dir: Path,
        variables: dict,
    ) -> None:
        """Render a template to the output directory."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise ValueError(f"Template '{template_name}' not found")

        # Add computed variables
        variables = self._compute_variables(variables)

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Set up Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(str(template_path)),
            keep_trailing_newline=True,
        )

        # Process all files in template directory
        self._render_directory(template_path, output_dir, env, variables)

    def _compute_variables(self, variables: dict) -> dict:
        """Compute derived variables."""
        result = dict(variables)

        # Compute package_name from project_name if not provided
        if "package_name" not in result and "project_name" in result:
            result["package_name"] = result["project_name"].replace("-", "_").lower()

        # Add timestamp
        result["now"] = datetime.now().isoformat()

        return result

    def _render_directory(
        self,
        src_dir: Path,
        dest_dir: Path,
        env: Environment,
        variables: dict,
    ) -> None:
        """Recursively render a directory."""
        for item in src_dir.iterdir():
            # Skip template.yml config file
            if item.name == "template.yml":
                continue

            # Render the filename (may contain variables)
            rendered_name = self._render_filename(item.name, variables)

            if item.is_dir():
                # Recursively process subdirectories
                new_dest = dest_dir / rendered_name
                new_dest.mkdir(parents=True, exist_ok=True)
                self._render_directory(item, new_dest, env, variables)
            else:
                # Process file
                dest_file = dest_dir / rendered_name
                dest_file.parent.mkdir(parents=True, exist_ok=True)

                if item.suffix == ".jinja":
                    # Render Jinja template
                    self._render_template_file(item, dest_file, env, variables, src_dir)
                else:
                    # Copy file as-is
                    shutil.copy2(item, dest_file)

    def _render_filename(self, filename: str, variables: dict) -> str:
        """Render variable placeholders in filename."""
        result = filename

        # Replace {{variable}} patterns
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))

        # Remove .jinja extension
        if result.endswith(".jinja"):
            result = result[:-6]

        return result

    def _render_template_file(
        self,
        src_file: Path,
        dest_file: Path,
        env: Environment,
        variables: dict,
        template_root: Path,
    ) -> None:
        """Render a single Jinja template file."""
        # Read and render the template content directly
        content = src_file.read_text()
        from jinja2 import Template

        template = Template(content)
        rendered = template.render(**variables)

        # Remove .jinja from destination filename
        final_dest = dest_file
        if str(dest_file).endswith(".jinja"):
            final_dest = Path(str(dest_file)[:-6])

        final_dest.write_text(rendered)

"""Tests for template renderer."""

from kraft.renderer import TemplateRenderer


class TestTemplateRenderer:
    """Tests for TemplateRenderer class."""

    def test_list_templates(self) -> None:
        renderer = TemplateRenderer()
        templates = renderer.list_templates()
        assert len(templates) >= 1
        assert any(t["name"] == "rest" for t in templates)

    def test_get_template_info_rest(self) -> None:
        renderer = TemplateRenderer()
        info = renderer.get_template_info("rest")
        assert info is not None
        assert info["name"] == "rest"
        assert "description" in info

    def test_get_template_info_nonexistent(self) -> None:
        renderer = TemplateRenderer()
        info = renderer.get_template_info("nonexistent")
        assert info is None

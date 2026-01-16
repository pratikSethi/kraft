"""Tests for UI module."""

from kraft.ui import ConsoleUI


class TestConsoleUI:
    """Tests for ConsoleUI class."""

    def test_ui_instantiation(self) -> None:
        ui = ConsoleUI()
        assert ui.console is not None

    def test_success_method_exists(self) -> None:
        ui = ConsoleUI()
        # Should not raise
        ui.success("Test message")

    def test_error_method_exists(self) -> None:
        ui = ConsoleUI()
        ui.error("Test error")

    def test_info_method_exists(self) -> None:
        ui = ConsoleUI()
        ui.info("Test info")

    def test_table_method_exists(self) -> None:
        ui = ConsoleUI()
        ui.table("Test", ["Col1", "Col2"], [["a", "b"]])

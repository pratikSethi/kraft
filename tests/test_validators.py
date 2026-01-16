"""Tests for input validation."""

from hypothesis import given
from hypothesis import strategies as st

from kraft.validators import validate_service_name


class TestValidateServiceName:
    """Tests for service name validation."""

    def test_valid_simple_name(self) -> None:
        result = validate_service_name("my-api")
        assert result.valid is True

    def test_valid_underscore_name(self) -> None:
        result = validate_service_name("user_service")
        assert result.valid is True

    def test_valid_mixed_name(self) -> None:
        result = validate_service_name("MyService123")
        assert result.valid is True

    def test_empty_name_rejected(self) -> None:
        result = validate_service_name("")
        assert result.valid is False
        assert "empty" in result.error.lower()

    def test_starts_with_number_rejected(self) -> None:
        result = validate_service_name("123service")
        assert result.valid is False
        assert "number" in result.error.lower()

    def test_spaces_rejected(self) -> None:
        result = validate_service_name("my service")
        assert result.valid is False
        assert result.suggestion is not None

    def test_special_chars_rejected(self) -> None:
        result = validate_service_name("my@service!")
        assert result.valid is False

    def test_too_long_rejected(self) -> None:
        result = validate_service_name("a" * 65)
        assert result.valid is False
        assert "long" in result.error.lower()


# Property-based test: Invalid names are rejected
@given(
    st.text(
        alphabet=st.sampled_from(" !@#$%^&*()+=[]{}|;:',.<>?/`~"),
        min_size=1,
        max_size=10,
    )
)
def test_special_char_names_rejected(name: str) -> None:
    """Property 3: Invalid service names with special chars are rejected."""
    result = validate_service_name(name)
    assert result.valid is False


@given(st.integers(min_value=0, max_value=999).map(str))
def test_numeric_start_rejected(num_prefix: str) -> None:
    """Names starting with numbers are rejected."""
    name = num_prefix + "service"
    result = validate_service_name(name)
    assert result.valid is False

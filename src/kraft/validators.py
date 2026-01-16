"""Input validation for kraft."""

import re
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check."""

    valid: bool
    error: str | None = None
    suggestion: str | None = None


def validate_service_name(name: str) -> ValidationResult:
    """Validate a service name.

    Rules:
    - Must not be empty
    - Must not start with a number
    - Only alphanumeric, hyphens, and underscores allowed
    - Must be 1-64 characters
    """
    if not name:
        return ValidationResult(
            valid=False,
            error="Service name cannot be empty",
            suggestion="Provide a name like 'my-api' or 'user_service'",
        )

    if len(name) > 64:
        return ValidationResult(
            valid=False,
            error=f"Service name too long ({len(name)} chars, max 64)",
            suggestion="Use a shorter name",
        )

    if name[0].isdigit():
        return ValidationResult(
            valid=False,
            error="Service name cannot start with a number",
            suggestion=f"Try '{name[0]}_{name}' or 'service_{name}'",
        )

    # Check for invalid characters
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        invalid_chars = set(re.findall(r"[^a-zA-Z0-9_-]", name))
        return ValidationResult(
            valid=False,
            error=f"Invalid characters: {', '.join(repr(c) for c in invalid_chars)}",
            suggestion="Use only letters, numbers, hyphens (-) and underscores (_)",
        )

    return ValidationResult(valid=True)

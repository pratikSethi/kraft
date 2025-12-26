# kraft

Python service scaffolding with zero learning curve.

## Installation

### Using uvx (one-time execution)
```bash
uvx kraft create my-api
```

### Using uv tool (persistent installation)
```bash
uv tool install kraft
kraft create my-api
```

### Using pip (traditional installation)
```bash
pip install kraft
kraft create my-api
```

## Shell Completion (Optional)

kraft supports shell completion for bash, zsh, and fish. To enable it:

```bash
# For bash
kraft --install-completion bash

# For zsh
kraft --install-completion zsh

# For fish
kraft --install-completion fish
```

After installation, restart your shell or reload your config. You'll then be able to use Tab to autocomplete commands and options.

## Development

### Setup

**Using uv (recommended):**
```bash
uv sync --extra dev
```

**Using pip:**
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# With uv
uv run pytest

# With pip (after activating venv)
pytest
```

### Linting

```bash
# With uv
uv run ruff check src/

# With pip (after activating venv)
ruff check src/
```

### Type Checking

```bash
# With uv
uv run mypy src/

# With pip (after activating venv)
mypy src/
```

## License

MIT

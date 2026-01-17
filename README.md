# kraft

Python service scaffolding with zero learning curve.

## Installation

### Using uvx (recommended - no installation needed)
```bash
uvx kraft
```

### Using uv tool (persistent installation)
```bash
uv tool install kraft-cli
kraft create my-api
```

### Using pipx (if you have it)
```bash
pipx install kraft-cli
kraft create my-api
```

### Using pip (traditional installation)

If you get "externally managed environment" error, try:

```bash
# Option 1: Install to user directory
pip3 install --user kraft-cli
kraft create my-api

# Option 2: Use pipx (install it first if needed)
pip3 install --user pipx
pipx install kraft-cli
kraft create my-api

# Option 3: Use a virtual environment
python3 -m venv ~/kraft-env
source ~/kraft-env/bin/activate
pip3 install kraft-cli
kraft create my-api
```

**Note:** If you get "externally managed environment" error with pip, use `uvx` or `uv tool install` instead.

## Usage

### Create a REST service

```bash
# Using uvx (no install needed)
uvx kraft-cli create my-api

# Or if you installed with uv tool/pipx
kraft create my-api
```

Then run it:
```bash
cd my-api
docker-compose up --build
```

Your API is now running at http://localhost:8000/books

### Add PostgreSQL database

```bash
kraft add postgres
# or: uvx kraft-cli add postgres
```

### Create with add-ons in one command

```bash
kraft create my-api --with postgres
```

### List available templates and add-ons

```bash
kraft list      # Show templates
kraft addons    # Show add-ons
```

## Shell Completion (Optional)

```bash
kraft --install-completion zsh
```

Restart your shell to enable Tab completion for commands and options.

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

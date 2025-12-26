# Design Document

## Overview

kraft is a Python CLI tool for scaffolding production-ready microservices with zero learning curve. The design emphasizes developer ergonomics through a "boring but working" philosophy - generating services that work immediately without requiring configuration or learning new patterns.

The architecture follows a modular, composable design where service templates and add-ons are independent layers that can be combined. This enables developers to start with a minimal service and incrementally add functionality (databases, message queues, observability) as needed.

**Key Design Principles:**
1. **Zero Configuration**: Generated services work immediately without setup
2. **Composability**: Add-ons are independent and can be combined freely
3. **Modern Tooling**: Use current Python ecosystem tools (uv, ruff, pytest, Rich)
4. **Visual Clarity**: Rich CLI output with colors, progress indicators, and formatted tables
5. **Copy-Paste Ready**: READMEs include working commands with actual ports and endpoints

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        kraft CLI                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Command    │  │   Template   │  │    Add-On    │      │
│  │   Parser     │──│   Engine     │──│   Manager    │      │
│  │   (Typer)    │  │  (Copier)    │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                   ┌────────▼────────┐                        │
│                   │  Rich Console   │                        │
│                   │  (UI/Output)    │                        │
│                   └─────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼──────┐
        │   Templates    │      │   Add-Ons   │
        │   Directory    │      │  Directory  │
        │                │      │             │
        │  - rest/       │      │ - postgres/ │
        │  - grpc/       │      │ - redis/    │
        │  - graphql/    │      │ - kafka/    │
        │                │      │ - observ./  │
        └────────────────┘      └─────────────┘
```

### Component Breakdown

**1. Command Parser (Typer)**
- Handles CLI argument parsing and validation
- Provides command routing (create, add, list, addons, show, init)
- Integrates with Rich for formatted output
- Validates user input before template generation

**2. Template Engine (Copier)**
- Renders service templates with variable substitution
- Manages template directory structure
- Handles file generation and updates
- Supports Jinja2 templating within Copier framework

**3. Add-On Manager**
- Applies add-ons to existing services
- Updates dependencies (pyproject.toml)
- Modifies docker-compose.yml
- Generates integration code
- Validates add-on compatibility

**4. Rich Console (UI Layer)**
- Provides colorful, formatted terminal output
- Displays progress bars for long operations
- Renders tables for template/add-on listings
- Shows success/error messages with icons
- Syntax highlights code snippets and file paths

## Components and Interfaces

### CLI Commands

```python
# Command structure using Typer

# Create service (minimal - defaults to REST)
kraft create <name> [--type <rest|grpc|graphql>] [--port PORT] [--no-docker] [--no-tests]

# Create service with add-ons in one command
kraft create <name> --with postgres --with redis --with observability  # Defaults to REST
kraft create <name> --type grpc --with postgres --with observability

# Add functionality incrementally
kraft add <addon> [--config CONFIG]
kraft add postgres redis kafka  # Multiple add-ons at once

# Discovery commands
kraft list
kraft addons
kraft show <template>

# Interactive wizard
kraft init

# Version
kraft --version
```

### Template Structure

Each service template follows this structure:

```
templates/
├── rest/
│   ├── copier.yml                    # Template configuration
│   ├── {{ project_name }}/
│   │   ├── pyproject.toml.jinja
│   │   ├── README.md.jinja
│   │   ├── Dockerfile.jinja
│   │   ├── docker-compose.yml.jinja
│   │   ├── .gitignore
│   │   ├── {{ package_name }}/
│   │   │   ├── __init__.py
│   │   │   ├── main.py.jinja
│   │   │   └── api/
│   │   │       ├── __init__.py
│   │   │       └── routes.py.jinja
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_api.py.jinja
├── grpc/
│   └── [similar structure]
└── graphql/
    └── [similar structure]
```

### Add-On Structure

```
addons/
├── postgres/
│   ├── addon.yml                     # Add-on metadata
│   ├── dependencies.txt              # Python packages to add
│   ├── docker-services.yml           # Docker compose services
│   ├── code/
│   │   ├── database.py.jinja         # Database connection module
│   │   └── models.py.jinja           # Example models
│   └── readme-section.md.jinja       # README documentation
├── redis/
├── kafka/
└── observability/
```

### Core Interfaces

**TemplateRenderer Interface:**
```python
class TemplateRenderer:
    def render(
        self,
        template_name: str,
        output_dir: Path,
        variables: dict[str, Any]
    ) -> None:
        """Render a template to the output directory using Jinja2."""
        
    def list_templates(self) -> list[TemplateInfo]:
        """List all available templates."""
        
    def get_template_info(self, template_name: str) -> TemplateInfo:
        """Get detailed information about a template."""
        
    def _copy_and_render_file(
        self,
        src: Path,
        dest: Path,
        variables: dict[str, Any]
    ) -> None:
        """Copy a file, rendering it with Jinja2 if it's a template."""
```

**AddOnManager Interface:**
```python
class AddOnManager:
    def apply_addon(
        self,
        addon_name: str,
        project_dir: Path,
        config: dict[str, Any] | None = None
    ) -> None:
        """Apply an add-on to an existing project."""
        
    def list_addons(self) -> list[AddOnInfo]:
        """List all available add-ons."""
        
    def validate_project(self, project_dir: Path) -> bool:
        """Validate that directory is a kraft project."""
```

**ConsoleUI Interface:**
```python
class ConsoleUI:
    def success(self, message: str) -> None:
        """Display success message with green color and checkmark."""
        
    def error(self, message: str, suggestion: str | None = None) -> None:
        """Display error message with red color and X icon."""
        
    def info(self, message: str) -> None:
        """Display info message with blue color and info icon."""
        
    def progress(self, description: str) -> ProgressContext:
        """Display progress bar or spinner."""
        
    def table(self, data: list[dict], columns: list[str]) -> None:
        """Display formatted table."""
```

## Data Models

### Template Configuration (template.yml)

```yaml
# Template metadata
name: "FastAPI REST Service"
description: "Production-ready REST API with FastAPI"
version: "1.0.0"

# Template variables with defaults
variables:
  project_name:
    type: str
    required: true
    description: "Name of your service (e.g., my-api)"
    pattern: "^[a-zA-Z][a-zA-Z0-9_-]*$"
  
  package_name:
    type: str
    default: "{{ project_name.replace('-', '_') }}"
  
  port:
    type: int
    default: 8000
    description: "Port for the service to listen on"
  
  python_version:
    type: str
    default: "3.11"
    choices: ["3.10", "3.11", "3.12"]
  
  include_docker:
    type: bool
    default: true
  
  include_tests:
    type: bool
    default: true
```

### Add-On Configuration (addon.yml)

```yaml
# Add-on metadata
name: "PostgreSQL"
description: "PostgreSQL database with SQLAlchemy ORM"
version: "1.0.0"

# Dependencies to add
dependencies:
  - "sqlalchemy>=2.0.0"
  - "psycopg2-binary>=2.9.0"
  - "alembic>=1.12.0"

# Docker services to add
docker_services:
  postgres:
    image: "postgres:16-alpine"
    environment:
      POSTGRES_USER: "{{ project_name }}"
      POSTGRES_PASSWORD: "dev_password"
      POSTGRES_DB: "{{ project_name }}_db"
    ports:
      - "5432:5432"
    volumes:
      - "postgres_data:/var/lib/postgresql/data"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {{ project_name }}"]
      interval: 5s
      timeout: 5s
      retries: 5

# Files to generate
files:
  - src: "code/database.py.jinja"
    dest: "{{ package_name }}/database.py"
  - src: "code/models.py.jinja"
    dest: "{{ package_name }}/models.py"

# README section to append
readme_section: "readme-section.md.jinja"
```

### Project Metadata (.kraft.yml)

Generated in each kraft project to track state:

```yaml
kraft_version: "0.1.0"
template: "rest"
template_version: "1.0.0"
created_at: "2024-12-25T10:30:00Z"
addons:
  - name: "postgres"
    version: "1.0.0"
    applied_at: "2024-12-25T10:35:00Z"
  - name: "observability"
    version: "1.0.0"
    applied_at: "2024-12-25T10:40:00Z"
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Service Generation Creates Correct Endpoints

*For any* service type (REST, gRPC, GraphQL) and any valid service name, generating a service should create a project with the appropriate working CRUD endpoints or methods for a books resource (REST: GET/POST/PUT/DELETE /books endpoints, gRPC: CRUD RPC methods, GraphQL: queries and mutations). When no type is specified, REST should be used as the default. Generated endpoints should include placeholder implementations with in-memory storage to demonstrate working CRUD operations.

**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.10**

### Property 2: Generated Services Include Required Files

*For any* generated service, the project directory should contain all required files: Dockerfile, docker-compose.yml, README.md, LICENSE, .env.example, unit tests, and proper Python package structure with __init__.py files.

**Validates: Requirements 1.5, 1.6, 1.7, 1.8, 5.8, 5.9**

### Property 3: Invalid Service Names Are Rejected

*For any* service name containing special characters (except hyphens and underscores) or spaces, the CLI should reject the input and display a helpful error message without creating any files.

**Validates: Requirements 1.9**

### Property 4: Add-Ons Apply Correctly

*For any* add-on (postgres, redis, kafka, observability) applied to a kraft-generated service, the add-on should add the correct dependencies, connection code, and example usage to the project.

**Validates: Requirements 2.3, 2.4, 2.5, 2.6**

### Property 4a: Services Can Be Created With Add-Ons

*For any* service type and any combination of add-ons specified via `--with` flags, the generated service should include all specified add-ons fully integrated (dependencies, code, docker services) as if they were added incrementally.

**Validates: Requirements 2.1, 2.2**

### Property 4b: Multiple Add-Ons Can Be Applied At Once

*For any* kraft-generated service and any list of add-ons provided to the `kraft add` command, all add-ons should be applied successfully in sequence.

**Validates: Requirements 2.7**

### Property 5: Add-Ons Update Project Files

*For any* add-on applied to a service, the CLI should update pyproject.toml with new dependencies, update docker-compose.yml with required services (if applicable), and create example code files.

**Validates: Requirements 2.8, 2.9, 2.10**

### Property 6: Add-Ons Require Kraft Project

*For any* directory that is not a kraft-generated service, attempting to apply an add-on should fail with a clear error message without modifying any files.

**Validates: Requirements 2.11**

### Property 7: Template Variable Substitution

*For any* generated service with custom configuration (service name, port, Python version), all template variables should be correctly substituted in all generated files (no placeholder text like {{ project_name }} should remain).

**Validates: Requirements 8.5**

### Property 8: Modern Python Tooling Configuration

*For any* generated service, the project should include pyproject.toml with semantic versioning (0.1.0), configuration for ruff and pytest, Python 3.10+ compatibility, .gitignore with Python patterns, LICENSE file with MIT license, .env.example for environment variables, and be installable via `uv pip install -e .`.

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9**

### Property 9: README Contains Required Sections

*For any* generated service, the README.md should contain all required sections: Overview, Setup, Running, Testing, API Endpoints, and a Quick Start section at the top.

**Validates: Requirements 7.1, 7.9**

### Property 10: README Includes Correct Test Commands

*For any* service type, the README should include the appropriate test commands (curl for REST, grpcurl for gRPC, GraphQL queries for GraphQL) using the actual configured port number, formatted in proper markdown code blocks.

**Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6**

### Property 11: README Updated With Add-On Documentation

*For any* add-on applied to a service, the README should be updated to include documentation for that add-on with example code showing how to use it.

**Validates: Requirements 7.8**

### Property 12: Docker Configuration Is Complete

*For any* generated service, the Docker configuration should include a multi-stage Dockerfile using uv for dependency installation, and a docker-compose.yml with health checks for all services.

**Validates: Requirements 9.1, 9.2, 9.4, 9.5**

### Property 13: Add-Ons Update Docker Compose

*For any* add-on requiring external services (postgres, redis, kafka), applying the add-on should update docker-compose.yml to include the required service containers with proper configuration.

**Validates: Requirements 9.3**

### Property 14: Generated Services Work Immediately

*For any* generated service, the service should work immediately: all included tests should pass, linting checks (ruff) should pass, Docker image should build successfully, docker-compose should start successfully, and the generated endpoint should respond correctly when the service is running.

**Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5**

### Property 15: Commands Provide Appropriate Feedback

*For any* command execution (success or failure), the CLI should display appropriate feedback: clear error messages with suggestions for failures, success messages with next steps for successes, and validation errors before attempting file generation for invalid input.

**Validates: Requirements 12.1, 12.2, 12.3, 12.5**

### Property 16: Custom Templates Can Be Loaded

*For any* user-specified template directory containing valid template structure, the CLI should be able to load and use those custom templates for service generation.

**Validates: Requirements 13.3**

## Error Handling

### Error Categories

**1. User Input Errors**
- Invalid service names (special characters, spaces)
- Invalid service types
- Invalid add-on names
- Missing required arguments

**Strategy:** Validate all input before any file operations. Display clear error messages with examples of valid input.

**2. File System Errors**
- Directory already exists
- Permission denied
- Disk full
- Invalid path

**Strategy:** Check preconditions before operations. Provide clear error messages with suggested actions (e.g., "Directory 'my-api' already exists. Use a different name or remove the existing directory.").

**3. Template Errors**
- Template not found
- Template rendering failure
- Invalid template configuration

**Strategy:** Validate templates during CLI startup. Fail fast with clear messages if templates are corrupted or missing.

**4. Add-On Errors**
- Add-on not found
- Not in a kraft project directory
- Add-on already applied
- Incompatible add-ons

**Strategy:** Validate project state before applying add-ons. Check for .kraft.yml metadata file. Provide clear guidance on resolution.

**5. External Tool Errors**
- Docker not installed
- uv not available
- Network errors (if fetching templates)

**Strategy:** Gracefully handle missing tools. Provide installation instructions. Allow operations to continue where possible (e.g., generate project even if Docker isn't installed, but warn user).

### Error Message Format

All error messages follow this structure using Rich formatting:

```
❌ Error: <Brief description>

<Detailed explanation>

💡 Suggestion: <Corrective action>
```

Example:
```
❌ Error: Invalid service name 'my api'

Service names cannot contain spaces. Use hyphens or underscores instead.

💡 Suggestion: Try 'my-api' or 'my_api'
```

### Rollback Strategy

For operations that modify files:
1. **Create operations**: If generation fails partway through, delete the partially created directory
2. **Add-on operations**: If add-on application fails, restore original files from backup
3. **Update operations**: Always backup files before modification

## Testing Strategy

### Dual Testing Approach

kraft will use both unit tests and property-based tests for comprehensive coverage:

**Unit Tests:**
- Specific examples of service generation
- Edge cases (empty directories, special characters)
- Error conditions (missing templates, invalid input)
- Integration points (CLI commands, file operations)

**Property-Based Tests:**
- Universal properties across all inputs
- Comprehensive input coverage through randomization
- Minimum 100 iterations per property test

### Property-Based Testing Configuration

**Library:** Hypothesis (Python's leading property-based testing library)

**Configuration:**
```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)
@given(
    service_name=st.text(
        alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd')),
        min_size=1,
        max_size=50
    ).filter(lambda s: s[0].isalpha()),
    service_type=st.sampled_from(['rest', 'grpc', 'graphql']),
    port=st.integers(min_value=1024, max_value=65535)
)
def test_property_1_service_generation(service_name, service_type, port):
    """
    Feature: kraft-cli, Property 1: Service Generation Creates Correct Endpoint
    
    For any service type and valid service name, generation creates
    the appropriate endpoint/method.
    """
    # Test implementation
```

**Test Organization:**
```
tests/
├── unit/
│   ├── test_cli_commands.py
│   ├── test_template_rendering.py
│   ├── test_addon_manager.py
│   └── test_console_ui.py
├── property/
│   ├── test_service_generation_properties.py
│   ├── test_addon_properties.py
│   ├── test_readme_properties.py
│   └── test_validation_properties.py
└── integration/
    ├── test_end_to_end_rest.py
    ├── test_end_to_end_grpc.py
    └── test_end_to_end_graphql.py
```

### Testing Generators

Custom Hypothesis strategies for kraft-specific data:

```python
# Valid service names
valid_service_names = st.text(
    alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd'), characters='-_'),
    min_size=1,
    max_size=50
).filter(lambda s: s[0].isalpha() and not s.endswith('-') and not s.endswith('_'))

# Invalid service names (for negative testing)
invalid_service_names = st.one_of(
    st.text(min_size=1).filter(lambda s: ' ' in s),  # Contains spaces
    st.text(min_size=1).filter(lambda s: any(c in s for c in '!@#$%^&*()')),  # Special chars
    st.just(''),  # Empty string
)

# Service types
service_types = st.sampled_from(['rest', 'grpc', 'graphql'])

# Add-ons
addons = st.sampled_from(['postgres', 'redis', 'kafka', 'observability'])

# Port numbers
ports = st.integers(min_value=1024, max_value=65535)
```

### Test Execution

**Local Development:**
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only property tests
pytest tests/property/

# Run with coverage
pytest --cov=kraft --cov-report=html
```

**CI/CD:**
- Run full test suite on every commit
- Property tests with 100 iterations minimum
- Integration tests in Docker containers
- Test on Python 3.10, 3.11, 3.12

## Implementation Notes

### Technology Choices

**CLI Framework: Typer**
- Built on Click, modern type-hint based API
- Automatic help generation
- Excellent integration with Rich
- Simpler than Click for new projects
- Use minimal `typer` package, not `typer[all]`

**Template Engine: Jinja2 (Direct)**
- Industry-standard Python templating
- Fast and well-documented
- No need for Copier wrapper - we'll implement simple file copying ourselves
- Reduces dependencies significantly

**UI Library: Rich**
- Beautiful terminal formatting
- Progress bars, tables, syntax highlighting
- Excellent documentation
- Active development

**Testing: Hypothesis + pytest**
- Industry-standard property-based testing
- Excellent Python integration
- Rich strategy library
- Good error reporting

### Minimal Dependencies

```toml
dependencies = [
    "typer>=0.9.0",      # CLI framework (minimal)
    "rich>=13.0.0",      # Terminal formatting
    "jinja2>=3.1.0",     # Template rendering
    "pyyaml>=6.0.0",     # YAML config parsing
]
```

**Why these are essential:**
- `typer`: CLI argument parsing and command routing
- `rich`: Beautiful terminal output (requirement 6.1-6.7)
- `jinja2`: Template variable substitution (requirement 8.5)
- `pyyaml`: Parse template and add-on configuration files

**What we're NOT using:**
- `copier`: Too heavyweight, we'll implement simple file copying ourselves
- `typer[all]`: Includes unnecessary extras, we only need core typer + rich

### Package Structure

```
kraft/
├── pyproject.toml
├── README.md
├── src/
│   └── kraft/
│       ├── __init__.py
│       ├── __main__.py              # Entry point
│       ├── cli.py                   # Typer CLI commands
│       ├── template_renderer.py     # Copier integration
│       ├── addon_manager.py         # Add-on application logic
│       ├── console_ui.py            # Rich UI wrapper
│       ├── validators.py            # Input validation
│       ├── models.py                # Data models
│       └── utils.py                 # Utilities
├── templates/
│   ├── rest/
│   ├── grpc/
│   └── graphql/
├── addons/
│   ├── postgres/
│   ├── redis/
│   ├── kafka/
│   └── observability/
└── tests/
    ├── unit/
    ├── property/
    └── integration/
```

### Distribution

**PyPI Package:**
```toml
[project]
name = "kraft"
version = "0.1.0"
description = "Python service scaffolding with zero learning curve"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "jinja2>=3.1.0",
    "pyyaml>=6.0.0",
]

[project.scripts]
kraft = "kraft.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Installation Methods:**
```bash
# One-time execution
uvx kraft create my-api --type rest

# Persistent installation
uv tool install kraft

# Traditional pip
pip install kraft
```

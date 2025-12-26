# Requirements Document

## Introduction

kraft is a Python service scaffolding CLI tool designed to empower developers to quickly create production-ready microservices with zero learning curve. The tool focuses on developer ergonomics, providing a "boring but working" approach to spinning up REST, gRPC, and GraphQL services with composable add-ons for databases, message queues, and observability.

The primary goal is to smoothen the learning curve for system design learners by making experimentation faster and easier through intelligent scaffolding.

## Glossary

- **kraft**: The CLI tool for scaffolding Python services
- **Service_Template**: A pre-configured project structure for a specific service type (REST, gRPC, GraphQL)
- **Add_On**: A composable layer that adds functionality (database, message queue, observability) to an existing service
- **CLI**: Command-line interface for interacting with kraft
- **Scaffold**: The process of generating a complete, working project structure from templates
- **uv**: Modern Python package installer and resolver (used for distribution)
- **FastAPI**: Python web framework for building REST APIs
- **Service_Type**: The architectural pattern of the service (REST, gRPC, or GraphQL)
- **Rich_CLI**: Terminal output with colors, formatting, and visual feedback using the Rich library
- **Copier**: Modern template engine alternative to Cookiecutter/Jinja2 with better UX
- **Semantic_Versioning**: Version numbering scheme (MAJOR.MINOR.PATCH) for kraft and generated services

## Requirements

### Requirement 1: Service Creation

**User Story:** As a developer, I want to create a new Python service with a single command, so that I can start building my application immediately without manual setup.

#### Acceptance Criteria

1. WHEN a user runs `kraft create <service-name>` without specifying a type, THE CLI SHALL generate a REST service with FastAPI as the default
2. WHEN a user runs `kraft create <service-name> --type rest`, THE CLI SHALL generate a complete FastAPI project with working CRUD endpoints for a books resource (GET /books, POST /books, GET /books/{id}, PUT /books/{id}, DELETE /books/{id})
3. WHEN a user runs `kraft create <service-name> --type grpc`, THE CLI SHALL generate a complete gRPC service with working CRUD RPC methods for a books resource
4. WHEN a user runs `kraft create <service-name> --type graphql`, THE CLI SHALL generate a complete GraphQL service with working queries and mutations for a books resource
5. WHEN a service is created, THE CLI SHALL include a Dockerfile and docker-compose.yml by default
6. WHEN a service is created, THE CLI SHALL include a README.md with instructions for running the service
7. WHEN a service is created, THE CLI SHALL include basic unit tests for the generated endpoints
8. WHEN a service is created, THE CLI SHALL use a valid Python project structure with proper package organization
9. WHEN a user provides an invalid service name (containing special characters or spaces), THE CLI SHALL reject the input and display a helpful error message
10. WHEN a service is created, THE generated endpoints SHALL include placeholder implementations with in-memory storage to demonstrate working CRUD operations

### Requirement 2: Add-On System

**User Story:** As a developer, I want to add functionality to my service incrementally or all at once, so that I can compose features as needed without starting from scratch.

#### Acceptance Criteria

1. WHEN a user runs `kraft create <name> --type rest --with postgres --with redis`, THE CLI SHALL generate a service with postgres and redis add-ons already integrated
2. WHEN a user runs `kraft create <name> --type rest --with observability`, THE CLI SHALL generate a service with observability add-on already integrated
3. WHEN a user runs `kraft add postgres` in a service directory, THE CLI SHALL add SQLAlchemy dependencies and database connection boilerplate
4. WHEN a user runs `kraft add redis` in a service directory, THE CLI SHALL add Redis client dependencies and connection configuration
5. WHEN a user runs `kraft add kafka` in a service directory, THE CLI SHALL add Kafka producer/consumer dependencies and example code
6. WHEN a user runs `kraft add observability` in a service directory, THE CLI SHALL add logging configuration and metrics collection (Prometheus/OpenTelemetry)
7. WHEN a user runs `kraft add postgres redis kafka`, THE CLI SHALL apply all three add-ons in sequence
8. WHEN an add-on is applied, THE CLI SHALL update the project's dependencies file (pyproject.toml or requirements.txt)
9. WHEN an add-on is applied, THE CLI SHALL update the docker-compose.yml to include necessary service containers
10. WHEN an add-on is applied, THE CLI SHALL create example code demonstrating how to use the added functionality
11. WHEN a user attempts to add an add-on outside a kraft-generated service directory, THE CLI SHALL display an error message

### Requirement 3: Template Discovery

**User Story:** As a developer, I want to discover available templates and add-ons, so that I know what options are available before creating a service.

#### Acceptance Criteria

1. WHEN a user runs `kraft list`, THE CLI SHALL display all available service templates with descriptions
2. WHEN a user runs `kraft addons`, THE CLI SHALL display all available add-ons with descriptions
3. WHEN a user runs `kraft show rest`, THE CLI SHALL display detailed information about the REST template including dependencies and structure
4. WHEN displaying templates or add-ons, THE CLI SHALL format output in a readable, organized manner

### Requirement 4: Interactive Mode

**User Story:** As a developer, I want an interactive wizard for creating services, so that I can make choices without memorizing command-line flags.

#### Acceptance Criteria

1. WHEN a user runs `kraft init`, THE CLI SHALL prompt for service name
2. WHEN a user runs `kraft init`, THE CLI SHALL prompt for service type with options (REST, gRPC, GraphQL)
3. WHEN a user runs `kraft init`, THE CLI SHALL prompt for optional add-ons with multi-select capability
4. WHEN a user runs `kraft init`, THE CLI SHALL prompt whether to include Docker configuration
5. WHEN the interactive wizard completes, THE CLI SHALL generate the service with all selected options

### Requirement 5: Project Structure and Dependencies

**User Story:** As a developer, I want generated projects to use modern Python tooling, so that my projects remain maintainable and follow current best practices.

#### Acceptance Criteria

1. THE CLI SHALL generate projects using pyproject.toml for dependency management
2. THE CLI SHALL include configuration for modern Python tools (ruff for linting, pytest for testing)
3. THE CLI SHALL generate projects compatible with Python 3.10+
4. THE CLI SHALL include a .gitignore file with appropriate Python exclusions
5. THE CLI SHALL generate projects that can be installed via `uv pip install -e .`
6. THE CLI SHALL use semantic versioning (0.1.0) as the initial version for generated services
7. THE CLI SHALL include version information in pyproject.toml following semantic versioning conventions
8. THE CLI SHALL include a LICENSE file with MIT license text in generated services
9. THE CLI SHALL include a .env.example file as a template for environment variables

### Requirement 6: Rich CLI Experience

**User Story:** As a developer, I want a visually appealing and informative CLI, so that I can easily understand what kraft is doing and enjoy using it.

#### Acceptance Criteria

1. THE CLI SHALL use the Rich library for colorful, formatted terminal output
2. WHEN displaying success messages, THE CLI SHALL use green color with appropriate icons
3. WHEN displaying error messages, THE CLI SHALL use red color with appropriate icons
4. WHEN displaying informational messages, THE CLI SHALL use blue color with appropriate icons
5. WHEN running long operations, THE CLI SHALL display progress bars or spinners
6. WHEN listing templates or add-ons, THE CLI SHALL use formatted tables with proper alignment
7. THE CLI SHALL use syntax highlighting when displaying code snippets or file paths

### Requirement 7: README Generation

**User Story:** As a developer, I want a well-formatted README with copy-paste commands, so that I can quickly understand and run my generated service.

#### Acceptance Criteria

1. WHEN a service is created, THE CLI SHALL generate a README.md with clear sections (Overview, Setup, Running, Testing, API Endpoints)
2. WHEN a REST service is created, THE README SHALL include curl commands for testing CRUD endpoints (e.g., `curl http://localhost:8000/books`, `curl -X POST http://localhost:8000/books -d '{"title":"Example","author":"Author"}'`)
3. WHEN a gRPC service is created, THE README SHALL include grpcurl commands for testing RPC methods
4. WHEN a GraphQL service is created, THE README SHALL include example GraphQL queries and mutations
5. THE README SHALL include the actual port number configured for the service in all example commands
6. THE README SHALL use code blocks with proper syntax highlighting for all commands
7. THE README SHALL be concise, focusing on essential information without overwhelming the user
8. WHEN add-ons are included, THE README SHALL document how to use each add-on with example code
9. THE README SHALL include a "Quick Start" section at the top with the minimal commands to run the service

### Requirement 8: Template Engine Selection

**User Story:** As a developer, I want kraft to use modern templating tools, so that the codebase remains maintainable and extensible.

#### Acceptance Criteria

1. THE CLI SHALL evaluate Copier as an alternative to Jinja2 for template rendering
2. WHERE Copier provides better developer experience, THE CLI SHALL use Copier for template management
3. WHERE Jinja2 is more appropriate, THE CLI SHALL use Jinja2 with clear documentation
4. THE CLI SHALL document the chosen template engine and rationale in developer documentation
5. THE template system SHALL support variable substitution for service names, ports, and configuration

### Requirement 9: Docker Integration

**User Story:** As a developer, I want Docker configuration included by default, so that I can run my service in containers immediately.

#### Acceptance Criteria

1. WHEN a service is created, THE CLI SHALL generate a multi-stage Dockerfile optimized for Python
2. WHEN a service is created, THE CLI SHALL generate a docker-compose.yml for local development
3. WHEN add-ons requiring external services are added (postgres, redis, kafka), THE CLI SHALL update docker-compose.yml with those services
4. THE Dockerfile SHALL use uv for dependency installation to ensure fast builds
5. THE docker-compose.yml SHALL include health checks for all services

### Requirement 10: CLI Distribution and Installation

**User Story:** As a developer, I want to install kraft easily, so that I can start using it without complex setup.

#### Acceptance Criteria

1. THE CLI SHALL be installable via `uvx kraft` for one-time execution
2. THE CLI SHALL be installable via `uv tool install kraft` for persistent installation
3. THE CLI SHALL be installable via `pip install kraft` for traditional installation
4. THE CLI SHALL be published to PyPI with proper metadata and versioning
5. WHEN kraft is installed, THE CLI SHALL be available as a `kraft` command in the user's PATH
6. THE kraft CLI SHALL follow semantic versioning (MAJOR.MINOR.PATCH)
7. THE kraft CLI SHALL include version information accessible via `kraft --version`

### Requirement 11: Template Validation

**User Story:** As a developer, I want generated services to work immediately, so that I can verify the scaffolding is correct before making changes.

#### Acceptance Criteria

1. WHEN a service is created, THE generated code SHALL pass all included tests
2. WHEN a service is created, THE generated code SHALL pass linting checks (ruff)
3. WHEN a service is created with Docker, THE service SHALL build successfully with `docker build`
4. WHEN a service is created with Docker, THE service SHALL start successfully with `docker-compose up`
5. WHEN a service is created, THE generated endpoint SHALL respond correctly when the service is running

### Requirement 12: Error Handling and User Feedback

**User Story:** As a developer, I want clear error messages and feedback, so that I can understand and fix issues quickly.

#### Acceptance Criteria

1. WHEN a command fails, THE CLI SHALL display a clear error message explaining what went wrong
2. WHEN a command fails, THE CLI SHALL suggest corrective actions when possible
3. WHEN a command succeeds, THE CLI SHALL display a success message with next steps
4. WHEN a long-running operation is in progress, THE CLI SHALL display progress indicators
5. WHEN a user provides invalid input, THE CLI SHALL display validation errors before attempting to generate files

### Requirement 13: Extensibility and Customization

**User Story:** As a developer, I want to customize templates, so that I can adapt kraft to my team's specific needs.

#### Acceptance Criteria

1. THE CLI SHALL store templates in a well-documented directory structure
2. THE CLI SHALL use the chosen template engine (Copier or Jinja2) with clear variable naming
3. WHERE custom templates are provided, THE CLI SHALL support loading templates from a user-specified directory
4. THE CLI SHALL document the template structure and available variables for customization

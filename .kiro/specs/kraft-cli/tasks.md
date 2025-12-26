# Implementation Plan: kraft CLI

## Overview

This implementation plan breaks down the kraft CLI development into discrete, incremental tasks. Each task builds on previous work, with checkpoints to ensure quality. The focus is on creating a working MVP with REST support first, then expanding to gRPC and GraphQL.

## Tasks

- [x] 1. Set up project structure and core dependencies
  - Create pyproject.toml with kraft package configuration
  - Add dependencies: typer, rich, jinja2, pyyaml (minimal set)
  - Add dev dependencies: pytest, hypothesis, ruff, mypy
  - Create src/kraft/ package structure with __init__.py, __main__.py
  - Set up basic CLI entry point with Typer
  - Configure ruff for linting and mypy for type checking
  - _Requirements: 5.1, 5.2, 10.6_

- [ ]* 1.1 Write unit tests for project structure
  - Test that package imports correctly
  - Test that CLI entry point is accessible
  - _Requirements: 5.1_

- [ ] 2. Implement Rich console UI wrapper
  - [ ] 2.1 Create ConsoleUI class with Rich integration
    - Implement success(), error(), info() methods with colored output
    - Implement progress() method for progress bars/spinners
    - Implement table() method for formatted table display
    - Add emoji icons for success (✅), error (❌), info (ℹ️)
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

  - [ ]* 2.2 Write unit tests for ConsoleUI
    - Test message formatting with colors
    - Test table rendering
    - _Requirements: 6.1_

- [ ] 3. Implement input validation
  - [ ] 3.1 Create validators module
    - Implement validate_service_name() function
    - Reject names with spaces or special characters (except - and _)
    - Reject names starting with numbers
    - Return clear error messages with suggestions
    - _Requirements: 1.9, 12.1, 12.2, 12.5_

  - [ ]* 3.2 Write property test for service name validation
    - **Property 3: Invalid Service Names Are Rejected**
    - **Validates: Requirements 1.9**
    - Generate invalid service names (spaces, special chars)
    - Verify all are rejected with error messages
    - _Requirements: 1.9_

  - [ ]* 3.3 Write unit tests for edge cases
    - Test empty string, very long names, unicode characters
    - _Requirements: 1.9_

- [ ] 4. Create REST service template
  - [ ] 4.1 Create templates/rest/ directory structure
    - Create template.yml with template configuration (not copier.yml)
    - Define variables: project_name, package_name, port, python_version
    - Add validation patterns for project_name
    - Set defaults: port=8000, python_version="3.11", include_docker=true
    - _Requirements: 1.2, 5.1_

  - [ ] 4.2 Create FastAPI service template files
    - Create pyproject.toml.jinja with FastAPI dependencies
    - Create main.py.jinja with FastAPI app
    - Create routes.py.jinja with CRUD endpoints for books resource (GET /books, POST /books, GET /books/{id}, PUT /books/{id}, DELETE /books/{id})
    - Include in-memory storage implementation to demonstrate working CRUD operations
    - Create models.py.jinja with Book data model (Pydantic)
    - Create __init__.py files for package structure
    - _Requirements: 1.2, 1.8, 1.10_

  - [ ] 4.3 Create Docker configuration templates
    - Create Dockerfile.jinja with multi-stage build using uv
    - Create docker-compose.yml.jinja with service definition
    - Add health checks to docker-compose.yml
    - _Requirements: 1.5, 9.1, 9.2, 9.4, 9.5_

  - [ ] 4.4 Create README template
    - Create README.md.jinja with sections: Overview, Quick Start, Setup, Running, Testing, API Endpoints
    - Include curl commands for CRUD operations (GET /books, POST /books with JSON body, GET /books/{id}, PUT /books/{id}, DELETE /books/{id})
    - Use actual {{ port }} variable in all commands
    - Use markdown code blocks with syntax highlighting
    - Add Quick Start section at top with minimal commands
    - _Requirements: 1.6, 7.1, 7.2, 7.5, 7.6, 7.9_

  - [ ] 4.5 Create test template
    - Create test_api.py.jinja with pytest tests for books CRUD endpoints
    - Include tests for GET /books (list), POST /books (create), GET /books/{id} (retrieve), PUT /books/{id} (update), DELETE /books/{id} (delete)
    - Test successful responses, status codes, and error cases (404 for non-existent books)
    - _Requirements: 1.7_

  - [ ] 4.6 Create supporting files
    - Create .gitignore with Python patterns
    - Create .kraft.yml.jinja for project metadata
    - Create LICENSE with MIT license text
    - Create .env.example with placeholder environment variables (empty for base template, populated by add-ons)
    - _Requirements: 5.4_

- [ ] 5. Implement template rendering engine
  - [ ] 5.1 Create TemplateRenderer class
    - Implement render() method using Copier
    - Implement list_templates() to discover available templates
    - Implement get_template_info() to read template metadata
    - Handle template rendering errors gracefully
    - _Requirements: 8.5_

  - [ ]* 5.2 Write property test for template rendering
    - **Property 7: Template Variable Substitution**
    - **Validates: Requirements 8.5**
    - Generate random service names, ports, versions
    - Verify no placeholder text remains in generated files
    - _Requirements: 8.5_

  - [ ]* 5.3 Write unit tests for template discovery
    - Test list_templates() returns REST template
    - Test get_template_info() returns correct metadata
    - _Requirements: 3.1, 3.3_

- [ ] 6. Implement kraft create command
  - [ ] 6.1 Create CLI command handler
    - Implement create command with Typer
    - Add parameters: name (required), --type (default="rest"), --port, --with (multiple), --no-docker, --no-tests
    - Validate service name before generation
    - Default to REST when --type not specified
    - _Requirements: 1.1, 1.2_

  - [ ] 6.2 Implement service generation logic
    - Call TemplateRenderer.render() with user inputs
    - Handle --with flags to apply add-ons during creation
    - Display progress with Rich progress bar
    - Show success message with next steps
    - Handle errors and display helpful messages
    - _Requirements: 1.1, 2.1, 2.2, 12.3_

  - [ ]* 6.3 Write property test for service generation
    - **Property 1: Service Generation Creates Correct Endpoints**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.10**
    - Generate services with random names and types
    - Verify CRUD endpoints exist in generated code (GET /books, POST /books, etc.)
    - Verify service defaults to REST when type not specified
    - Verify in-memory storage implementation present
    - _Requirements: 1.1, 1.2, 1.10_

  - [ ]* 6.4 Write property test for required files
    - **Property 2: Generated Services Include Required Files**
    - **Validates: Requirements 1.5, 1.6, 1.7, 1.8, 5.8, 5.9**
    - Generate services with random configurations
    - Verify Dockerfile, docker-compose.yml, README.md, LICENSE, .env.example, tests exist
    - Verify proper package structure with __init__.py files
    - _Requirements: 1.5, 1.6, 1.7, 1.8, 5.8, 5.9_

- [ ] 7. Checkpoint - Ensure basic service generation works
  - Manually test: kraft create my-api
  - Verify generated service structure
  - Verify README has correct curl commands for CRUD operations
  - Test CRUD endpoints work (create book, list books, get book, update book, delete book)
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement add-on system
  - [ ] 8.1 Create postgres add-on
    - Create addons/postgres/ directory
    - Create addon.yml with metadata and dependencies
    - Create docker-services.yml with postgres container config
    - Create database.py.jinja with SQLAlchemy connection code
    - Create models.py.jinja with example model
    - Create readme-section.md.jinja with usage documentation
    - _Requirements: 2.3_

  - [ ] 8.2 Create redis add-on
    - Create addons/redis/ directory
    - Create addon.yml with metadata and dependencies
    - Create docker-services.yml with redis container config
    - Create redis_client.py.jinja with connection code
    - Create readme-section.md.jinja with usage documentation
    - _Requirements: 2.4_

  - [ ] 8.3 Create observability add-on
    - Create addons/observability/ directory
    - Create addon.yml with metadata and dependencies
    - Create logging_config.py.jinja with structured logging setup
    - Create metrics.py.jinja with Prometheus metrics
    - Create readme-section.md.jinja with usage documentation
    - _Requirements: 2.6_

  - [ ] 8.4 Create AddOnManager class
    - Implement apply_addon() method
    - Update pyproject.toml with new dependencies
    - Update docker-compose.yml with new services
    - Generate code files from add-on templates
    - Append add-on documentation to README
    - Update .kraft.yml with applied add-on metadata
    - Validate project is a kraft project before applying
    - _Requirements: 2.8, 2.9, 2.10, 2.11_

  - [ ]* 8.5 Write property test for add-on application
    - **Property 4: Add-Ons Apply Correctly**
    - **Validates: Requirements 2.3, 2.4, 2.5, 2.6**
    - Generate service, apply random add-ons
    - Verify dependencies added to pyproject.toml
    - Verify code files created
    - _Requirements: 2.3, 2.4, 2.5, 2.6_

  - [ ]* 8.6 Write property test for project file updates
    - **Property 5: Add-Ons Update Project Files**
    - **Validates: Requirements 2.8, 2.9, 2.10**
    - Apply add-ons requiring docker services
    - Verify docker-compose.yml updated
    - Verify README updated with add-on docs
    - _Requirements: 2.8, 2.9, 2.10_

  - [ ]* 8.7 Write property test for non-kraft directory
    - **Property 6: Add-Ons Require Kraft Project**
    - **Validates: Requirements 2.11**
    - Attempt to apply add-on in empty directory
    - Verify error message displayed
    - Verify no files modified
    - _Requirements: 2.11_

- [ ] 9. Implement kraft add command
  - [ ] 9.1 Create CLI command handler
    - Implement add command with Typer
    - Accept multiple add-on names as arguments
    - Validate current directory is a kraft project
    - Call AddOnManager.apply_addon() for each add-on
    - Display progress and success messages
    - _Requirements: 2.3, 2.7_

  - [ ]* 9.2 Write property test for multiple add-ons
    - **Property 4b: Multiple Add-Ons Can Be Applied At Once**
    - **Validates: Requirements 2.7**
    - Generate service, apply multiple add-ons in one command
    - Verify all add-ons applied successfully
    - _Requirements: 2.7_

- [ ] 10. Implement --with flag for create command
  - [ ] 10.1 Update create command to handle --with flags
    - Parse --with flags into list of add-ons
    - After template rendering, apply each add-on
    - Display progress for each add-on
    - _Requirements: 2.1, 2.2_

  - [ ]* 10.2 Write property test for combined creation
    - **Property 4a: Services Can Be Created With Add-Ons**
    - **Validates: Requirements 2.1, 2.2**
    - Generate services with random --with flags
    - Verify add-ons fully integrated
    - Verify equivalent to incremental addition
    - _Requirements: 2.1, 2.2_

- [ ] 11. Checkpoint - Ensure add-on system works
  - Manually test: kraft create my-api --with postgres --with redis
  - Manually test: kraft add observability in existing project
  - Verify docker-compose.yml updated correctly
  - Verify README updated with add-on documentation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement discovery commands
  - [ ] 12.1 Implement kraft list command
    - Display table of available templates using Rich
    - Show template name, description, version
    - _Requirements: 3.1_

  - [ ] 12.2 Implement kraft addons command
    - Display table of available add-ons using Rich
    - Show add-on name, description, dependencies
    - _Requirements: 3.2_

  - [ ] 12.3 Implement kraft show command
    - Display detailed template information
    - Show dependencies, structure, configuration options
    - _Requirements: 3.3_

  - [ ]* 12.4 Write unit tests for discovery commands
    - Test list command output
    - Test addons command output
    - Test show command output
    - _Requirements: 3.1, 3.2, 3.3_

- [ ] 13. Implement README generation properties
  - [ ]* 13.1 Write property test for README sections
    - **Property 9: README Contains Required Sections**
    - **Validates: Requirements 7.1, 7.9**
    - Generate services with random configurations
    - Verify README contains all required sections
    - Verify Quick Start section at top
    - _Requirements: 7.1, 7.9_

  - [ ]* 13.2 Write property test for README commands
    - **Property 10: README Includes Correct Test Commands**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6**
    - Generate REST services with random ports
    - Verify curl commands use actual port
    - Verify commands in markdown code blocks
    - _Requirements: 7.2, 7.5, 7.6_

  - [ ]* 13.3 Write property test for README add-on docs
    - **Property 11: README Updated With Add-On Documentation**
    - **Validates: Requirements 7.8**
    - Apply add-ons to services
    - Verify README updated with add-on documentation
    - _Requirements: 7.8_

- [ ] 14. Implement Docker configuration properties
  - [ ]* 14.1 Write property test for Docker files
    - **Property 12: Docker Configuration Is Complete**
    - **Validates: Requirements 9.1, 9.2, 9.4, 9.5**
    - Generate services with random configurations
    - Verify Dockerfile has multi-stage build with uv
    - Verify docker-compose.yml has health checks
    - _Requirements: 9.1, 9.2, 9.4, 9.5_

  - [ ]* 14.2 Write property test for add-on Docker updates
    - **Property 13: Add-Ons Update Docker Compose**
    - **Validates: Requirements 9.3**
    - Apply add-ons requiring external services
    - Verify docker-compose.yml updated with service containers
    - _Requirements: 9.3_

- [ ] 15. Implement validation properties
  - [ ]* 15.1 Write property test for generated service validation
    - **Property 14: Generated Services Work Immediately**
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5**
    - Generate services with random configurations
    - Run pytest - verify tests pass
    - Run ruff - verify linting passes
    - Run docker build - verify builds successfully
    - Run docker-compose up - verify starts successfully
    - Test endpoint - verify responds correctly
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 16. Implement error handling properties
  - [ ]* 16.1 Write property test for command feedback
    - **Property 15: Commands Provide Appropriate Feedback**
    - **Validates: Requirements 12.1, 12.2, 12.3, 12.5**
    - Trigger various errors (invalid input, missing files)
    - Verify error messages with suggestions displayed
    - Trigger successful operations
    - Verify success messages with next steps displayed
    - _Requirements: 12.1, 12.2, 12.3, 12.5_

- [ ] 17. Implement modern Python tooling properties
  - [ ]* 17.1 Write property test for project configuration
    - **Property 8: Modern Python Tooling Configuration**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9**
    - Generate services with random configurations
    - Verify pyproject.toml exists with semantic versioning
    - Verify ruff and pytest configured
    - Verify Python 3.10+ compatibility
    - Verify .gitignore, LICENSE, .env.example exist
    - Verify installable via uv pip install -e .
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9_

- [ ] 18. Implement kraft --version command
  - [ ] 18.1 Add version command
    - Display kraft version using Rich
    - Read version from pyproject.toml
    - _Requirements: 10.7_

- [ ] 19. Implement kraft init interactive wizard
  - [ ] 19.1 Create interactive prompts
    - Prompt for service name with validation
    - Prompt for service type with choices (REST, gRPC, GraphQL)
    - Prompt for add-ons with multi-select
    - Prompt for Docker inclusion (yes/no)
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 19.2 Generate service from wizard inputs
    - Call create command with collected inputs
    - Display progress and success messages
    - _Requirements: 4.5_

  - [ ]* 19.3 Write unit tests for interactive wizard
    - Test prompts appear correctly
    - Test service generated with selected options
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 20. Checkpoint - Ensure all core features work
  - Test all CLI commands manually
  - Verify all property tests pass
  - Verify generated services work end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 21. Add gRPC service template
  - [ ] 21.1 Create templates/grpc/ directory structure
    - Create copier.yml with template configuration
    - Create proto file template with CRUD RPC methods for books resource (ListBooks, GetBook, CreateBook, UpdateBook, DeleteBook)
    - Create gRPC server implementation template with in-memory storage
    - Create Dockerfile and docker-compose.yml templates
    - Create README with grpcurl commands for CRUD operations
    - Create test template
    - _Requirements: 1.3, 1.10_

  - [ ]* 21.2 Update property tests to include gRPC
    - Update Property 1 test to generate gRPC services
    - Verify CRUD RPC methods exist (ListBooks, GetBook, CreateBook, UpdateBook, DeleteBook)
    - Verify in-memory storage implementation present
    - _Requirements: 1.3, 1.10_

- [ ] 22. Add GraphQL service template
  - [ ] 22.1 Create templates/graphql/ directory structure
    - Create copier.yml with template configuration
    - Create GraphQL schema template with queries (books, book) and mutations (createBook, updateBook, deleteBook)
    - Create resolver implementation template with in-memory storage
    - Create Dockerfile and docker-compose.yml templates
    - Create README with example GraphQL queries and mutations
    - Create test template
    - _Requirements: 1.4, 1.10_

  - [ ]* 22.2 Update property tests to include GraphQL
    - Update Property 1 test to generate GraphQL services
    - Verify queries (books, book) and mutations (createBook, updateBook, deleteBook) exist in schema
    - Verify in-memory storage implementation present
    - _Requirements: 1.4, 1.10_

- [ ] 23. Add kafka add-on
  - [ ] 23.1 Create addons/kafka/ directory
    - Create addon.yml with metadata and dependencies
    - Create docker-services.yml with kafka and zookeeper
    - Create producer.py.jinja and consumer.py.jinja templates
    - Create readme-section.md.jinja with usage documentation
    - _Requirements: 2.5_

  - [ ]* 23.2 Update property tests to include kafka
    - Update Property 4 test to apply kafka add-on
    - Verify kafka dependencies and code added
    - _Requirements: 2.5_

- [ ] 24. Implement custom template loading
  - [ ] 24.1 Add --template-dir flag to create command
    - Accept custom template directory path
    - Validate template directory structure
    - Load templates from custom directory
    - _Requirements: 13.3_

  - [ ]* 24.2 Write property test for custom templates
    - **Property 16: Custom Templates Can Be Loaded**
    - **Validates: Requirements 13.3**
    - Create custom template directory
    - Generate service using custom template
    - Verify service generated correctly
    - _Requirements: 13.3_

- [ ] 25. Final checkpoint - Complete system validation
  - Run full test suite (unit + property + integration)
  - Test all service types (REST, gRPC, GraphQL)
  - Test all add-ons (postgres, redis, kafka, observability)
  - Test all CLI commands
  - Verify generated services work end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 26. Prepare for PyPI distribution
  - [ ] 26.1 Update pyproject.toml for distribution
    - Add project metadata (description, authors, license)
    - Add project URLs (homepage, repository, documentation)
    - Configure build system (hatchling)
    - Add project.scripts entry point
    - _Requirements: 10.4_

  - [ ] 26.2 Create distribution documentation
    - Create comprehensive README.md for PyPI
    - Add installation instructions (uvx, uv tool, pip)
    - Add usage examples
    - Add contributing guidelines
    - _Requirements: 10.1, 10.2, 10.3_

  - [ ] 26.3 Test installation methods
    - Test uvx kraft (one-time execution)
    - Test uv tool install kraft (persistent)
    - Test pip install kraft (traditional)
    - Verify kraft command available in PATH
    - _Requirements: 10.1, 10.2, 10.3, 10.5_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Focus on REST + core add-ons first, then expand to gRPC/GraphQL

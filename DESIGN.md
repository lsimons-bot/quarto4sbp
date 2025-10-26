# Design Decisions

This document captures key design decisions for the quarto4sbp project. For detailed feature specifications, see the [specs directory](docs/spec/).

## Core Philosophy
- **Dependency-free core**: Core functionality uses only Python3 standard library (os, sys, datetime, argparse, unittest)
- **Organized structure**: Main code in `quarto4sbp/`, tests in `tests/`, configuration in `etc/`
- **Functional approach**: Avoids OOP, uses simple functions for clarity and maintainability

## Error Handling & Reliability
- **Graceful degradation**: Continue execution when individual tasks fail, with clear error messages
- **Exit codes**: 0 for success/already-ran, 1 for errors, 2 for test failures
- **User-friendly errors**: Print descriptive messages, avoid stack traces for expected failures
- **File operations**: Create parent directories automatically, handle permissions gracefully
- **Subprocess calls**: Use `check=True` and catch `CalledProcessError` with context

## Testing Strategy
- **Integration-first**: Prefer end-to-end tests over mocking for reliability
- **Test separation**: Unit tests in dedicated `tests/` directory using Python's unittest framework
- **CLI testing**: Test both standalone execution and programmatic usage
- **Temporary directories**: Use temp paths for file system tests to avoid conflicts

## Code Quality
- **Type safety**: Comprehensive type annotations for better IDE support and static analysis
- **Acceptable diagnostics**: Some remaining warnings for argparse/unittest patterns that are inherently dynamic
- **Pyright ignores**: Use specific error codes (`reportAny`, `reportImplicitOverride`) when needed

## Development Process
- **Spec-driven development**: New features documented in `docs/spec/` before implementation
- **Concise specs**: Focus on design decisions, reference shared patterns, avoid implementation details
- **Design documentation**: This file updated with architectural decisions made during feature implementation

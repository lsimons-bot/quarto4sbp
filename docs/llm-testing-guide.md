# LLM Testing Guide

This guide explains how to write tests for LLM-powered features using the mock-based testing infrastructure.

## Overview

The LLM testing infrastructure provides a fast, reliable, and cost-free way to test LLM-powered features without making real API calls. It consists of:

- **MockLLMClient**: A mock LLM client that returns canned responses
- **Fixture System**: Pre-configured response files for common use cases
- **Pytest Fixtures**: Ready-to-use test fixtures for different scenarios
- **Assertion Helpers**: Functions to verify LLM interactions

**Key Benefits:**
- ✅ Fast tests (no network calls)
- ✅ Deterministic results (no API variability)
- ✅ No API costs
- ✅ Works offline
- ✅ CI-friendly (no rate limits)

## Quick Start

### Basic Test Example

```python
def test_simple_llm_interaction(mock_llm):
    """Test a basic LLM prompt-response interaction."""
    # When
    response = mock_llm.prompt("hello")
    
    # Then
    assert "test LLM" in response
    assert_llm_call_count(mock_llm, 1)
```

### Custom Response Example

```python
def test_custom_responses(mock_llm_empty):
    """Test with custom response configuration."""
    # Given
    mock_llm_empty.add_response("analyze code", "The code looks good!")
    
    # When
    result = mock_llm_empty.prompt("analyze code")
    
    # Then
    assert result == "The code looks good!"
```

### Regex Pattern Example

```python
def test_regex_pattern(mock_llm_empty):
    """Test using regex patterns for flexible matching."""
    # Given
    mock_llm_empty.add_response(r"(write|create).*function", "def example(): pass")
    
    # When
    result1 = mock_llm_empty.prompt("write a function")
    result2 = mock_llm_empty.prompt("create a function")
    
    # Then
    assert "def example()" in result1
    assert "def example()" in result2
```

## MockLLMClient

The `MockLLMClient` is the core mock object that simulates LLM API interactions.

### Initialization

```python
from tests.mocks.llm_client import MockLLMClient

# Empty mock
mock = MockLLMClient()

# Mock with pre-configured responses
mock = MockLLMClient({
    "hello": "Hello! I'm a test LLM.",
    r"what.*name": "I'm a mock LLM client."
})
```

### Core Methods

#### `prompt(prompt_text: str, **kwargs) -> str`

Send a prompt and receive a response.

```python
response = mock.prompt("analyze this code")
```

The mock will:
1. Try exact string match first
2. Try regex pattern matches
3. Return default response if no match
4. Raise `ValueError` if no match and no default

#### `add_response(pattern: str, response: str) -> None`

Add a response mapping for a prompt pattern.

```python
# Exact match
mock.add_response("hello", "Hi there!")

# Regex pattern (case-insensitive)
mock.add_response(r"(analyze|review).*code", "Code looks good!")
```

#### `set_default_response(response: str) -> None`

Set a fallback response for unmatched prompts.

```python
mock.set_default_response("I don't understand that prompt.")
```

### Call History Methods

#### `get_call_count() -> int`

Get the total number of calls made.

```python
count = mock.get_call_count()
```

#### `get_last_call() -> dict | None`

Get the most recent call record.

```python
last_call = mock.get_last_call()
if last_call:
    print(last_call["prompt"])
```

#### `was_called_with(pattern: str) -> bool`

Check if any call matches a regex pattern.

```python
if mock.was_called_with(r"analyze"):
    print("Analysis was requested")
```

#### `get_calls_matching(pattern: str) -> list[dict]`

Get all calls matching a pattern.

```python
analyses = mock.get_calls_matching(r"analyze")
for call in analyses:
    print(call["prompt"])
```

#### `clear_history() -> None`

Clear the call history (useful for test setup/teardown).

```python
mock.clear_history()
```

## Fixture System

Fixtures are pre-written response files stored in `tests/fixtures/llm/` organized by category.

### Directory Structure

```
tests/fixtures/llm/
├── common/          # General-purpose responses
│   └── hello.txt
├── tov/             # Tone-of-voice responses
│   ├── rewrite-formal.txt
│   └── rewrite-casual.txt
└── viz/             # Visualization responses
    ├── analyze-slide.json
    └── generate-prompt.txt
```

### Loading Fixtures

#### `load_fixture_response(category: str, name: str) -> str`

Load a fixture file as a string.

```python
from tests.helpers.llm import load_fixture_response

# Load text fixture
hello = load_fixture_response("common", "hello")

# Load JSON fixture (as string)
analysis = load_fixture_response("viz", "analyze-slide")
```

#### `load_fixture_json(category: str, name: str) -> dict`

Load a JSON fixture as a parsed dictionary.

```python
from tests.helpers.llm import load_fixture_json

# Load and parse JSON
data = load_fixture_json("viz", "analyze-slide")
assert data["slide_type"] == "bullet_list"
```

#### `load_all_fixtures(category: str) -> dict[str, str]`

Load all fixtures from a category.

```python
from tests.helpers.llm import load_all_fixtures

# Load all common fixtures
fixtures = load_all_fixtures("common")
mock = MockLLMClient(fixtures)
```

### Creating New Fixtures

1. Choose or create a category directory in `tests/fixtures/llm/`
2. Create a `.txt` or `.json` file with the response content
3. Use descriptive names (e.g., `rewrite-formal.txt`, `analyze-slide.json`)

**Example text fixture** (`tests/fixtures/llm/tov/rewrite-casual.txt`):

```
Hey team! 👋

Quick update on what we've been working on...
```

**Example JSON fixture** (`tests/fixtures/llm/viz/analyze-slide.json`):

```json
{
  "slide_type": "bullet_list",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "suggested_visual": "icon_list"
}
```

## Pytest Fixtures

Six pre-configured pytest fixtures are available in `tests/conftest.py`.

### `mock_llm`

Basic mock with common test responses.

```python
def test_basic(mock_llm):
    response = mock_llm.prompt("hello")
    assert "test LLM" in response
```

**Pre-configured patterns:**
- `"hello"` → "Hello! I'm a test LLM."
- `r"what.*name"` → "I'm a mock LLM client for testing."
- `r"test"` → "This is a test response."

### `mock_llm_common`

Mock with all fixtures from the `common` category loaded.

```python
def test_common_fixture(mock_llm_common):
    response = mock_llm_common.prompt("hello")
    # Response comes from common/hello.txt
```

### `mock_llm_tov`

Mock configured for tone-of-voice testing.

```python
def test_formal_tone(mock_llm_tov):
    result = mock_llm_tov.prompt("Rewrite in formal tone: hey there!")
    # Response comes from tov/rewrite-formal.txt
```

**Pre-configured patterns:**
- `r"formal|professional|executive"` → formal tone fixture
- `r"casual|informal|friendly"` → casual tone fixture

### `mock_llm_viz`

Mock configured for visualization and image generation testing.

```python
def test_slide_analysis(mock_llm_viz):
    result = mock_llm_viz.prompt("Analyze this slide content")
    # Response comes from viz/analyze-slide.json
```

**Pre-configured patterns:**
- `r"analyze|analysis|slide"` → slide analysis fixture
- `r"image|visual|generate.*prompt"` → image prompt fixture

### `mock_llm_empty`

Empty mock for custom configuration in tests.

```python
def test_custom_setup(mock_llm_empty):
    mock_llm_empty.add_response("my pattern", "my response")
    result = mock_llm_empty.prompt("my pattern")
    assert result == "my response"
```

### `mock_llm_with_history`

Mock with pre-populated call history for testing history-dependent features.

```python
def test_with_history(mock_llm_with_history):
    # Already has 3 calls in history
    assert mock_llm_with_history.get_call_count() == 3
    
    # Add more calls
    mock_llm_with_history.prompt("new call")
    assert mock_llm_with_history.get_call_count() == 4
```

## Assertion Helpers

Helper functions for common test assertions in `tests/helpers/llm.py`.

### `assert_llm_called_with(mock, pattern: str)`

Assert the LLM was called with a prompt matching the pattern.

```python
from tests.helpers.llm import assert_llm_called_with

mock.prompt("analyze this code")
assert_llm_called_with(mock, r"analyze")  # ✅ Passes
assert_llm_called_with(mock, r"delete")   # ❌ Fails
```

### `assert_llm_not_called_with(mock, pattern: str)`

Assert the LLM was NOT called with a prompt matching the pattern.

```python
from tests.helpers.llm import assert_llm_not_called_with

mock.prompt("read data")
assert_llm_not_called_with(mock, r"delete")  # ✅ Passes
assert_llm_not_called_with(mock, r"read")    # ❌ Fails
```

### `assert_llm_call_count(mock, expected: int)`

Assert the exact number of LLM calls made.

```python
from tests.helpers.llm import assert_llm_call_count

mock.prompt("call 1")
mock.prompt("call 2")
assert_llm_call_count(mock, 2)  # ✅ Passes
assert_llm_call_count(mock, 3)  # ❌ Fails
```

### `get_llm_call_prompts(mock) -> list[str]`

Get a list of all prompts from the call history.

```python
from tests.helpers.llm import get_llm_call_prompts

mock.prompt("first")
mock.prompt("second")
prompts = get_llm_call_prompts(mock)
assert prompts == ["first", "second"]
```

## Writing Tests

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_feature(mock_llm_empty):
    """Test description."""
    # Arrange: Set up mock responses
    mock_llm_empty.add_response(r"analyze", "Analysis result")
    
    # Act: Call the code under test
    result = my_function(mock_llm_empty)
    
    # Assert: Verify behavior
    assert result == expected_value
    assert_llm_called_with(mock_llm_empty, r"analyze")
```

### Testing Tone-of-Voice Features

```python
def test_formal_rewrite(mock_llm_tov):
    """Test converting casual text to formal tone."""
    # Given
    casual = "Hey, check this out!"
    
    # When
    formal = rewrite_formal(casual, mock_llm_tov)
    
    # Then
    assert len(formal) > 0
    assert_llm_called_with(mock_llm_tov, r"formal")
```

### Testing Visualization Features

```python
def test_slide_analysis(mock_llm_viz):
    """Test analyzing slide content."""
    # Given
    slide_content = "# Title\n- Point 1\n- Point 2"
    
    # When
    analysis = analyze_slide(slide_content, mock_llm_viz)
    
    # Then
    assert analysis["slide_type"] == "bullet_list"
    assert_llm_called_with(mock_llm_viz, r"analyze")
```

### Testing Call Order

```python
def test_multi_step_process(mock_llm_empty):
    """Test a process that makes multiple LLM calls."""
    # Given
    mock_llm_empty.add_response(r"step 1", "Result 1")
    mock_llm_empty.add_response(r"step 2", "Result 2")
    
    # When
    process_data(mock_llm_empty)
    
    # Then
    prompts = get_llm_call_prompts(mock_llm_empty)
    assert "step 1" in prompts[0]
    assert "step 2" in prompts[1]
```

### Testing Error Handling

```python
def test_error_handling(mock_llm_empty):
    """Test handling of LLM errors."""
    # Given: Mock with no responses and no default
    # (will raise ValueError on unknown prompts)
    
    # When/Then: Should handle error gracefully
    result = safe_llm_call(mock_llm_empty, "unknown prompt")
    assert result is None  # Or whatever your error handling does
```

## Examples

The project includes 19 comprehensive example tests in `tests/test_llm_examples.py`.

### Running Examples

Examples are skipped by default. To run them:

```bash
RUN_EXAMPLE_TESTS=1 uv run pytest tests/test_llm_examples.py -v
```

### Example Categories

1. **Basic LLM Usage** (`TestBasicLLMUsage`)
   - Simple prompt-response interactions
   - Custom response mappings
   - Regex pattern matching

2. **Tone-of-Voice Rewriting** (`TestToneOfVoiceRewriting`)
   - Formal tone conversion
   - Casual tone conversion
   - Multiple tone conversions

3. **Visualization and Image Generation** (`TestVisualizationAndImageGeneration`)
   - Slide analysis
   - Image prompt generation
   - Multiple visualizations

4. **Call History and Assertions** (`TestCallHistoryAndAssertions`)
   - Verifying specific prompts
   - Verifying call order
   - Verifying call counts
   - Verifying no unwanted calls

5. **Fixture Integration** (`TestFixtureIntegration`)
   - Loading fixtures into mocks
   - Structured JSON responses
   - Multiple category fixtures

6. **Advanced Patterns** (`TestAdvancedPatterns`)
   - Conditional responses
   - Stateful interactions
   - Clearing and restarting

## Best Practices

### ✅ Do

- **Use specific pytest fixtures** for your use case (e.g., `mock_llm_tov` for tone-of-voice tests)
- **Use regex patterns** for flexible matching instead of exact strings
- **Verify call patterns** with assertion helpers, not just response content
- **Load fixtures** for realistic response content
- **Clear history** between test cases if needed
- **Test edge cases** like missing patterns or malformed responses
- **Keep fixtures small** and focused on one scenario

### ❌ Don't

- **Don't make real API calls** in unit tests (use integration tests instead)
- **Don't hardcode long responses** in test code (use fixtures)
- **Don't test implementation details** of the mock itself
- **Don't skip verification** of LLM calls (always assert they happened)
- **Don't reuse mocks** between tests without clearing history
- **Don't use overly complex regex** patterns (keep them readable)

### Pattern Matching Tips

**Exact matching** (fastest, most specific):
```python
mock.add_response("exact prompt text", "response")
```

**Regex matching** (flexible, case-insensitive by default):
```python
# Match variations
mock.add_response(r"(write|create|make)", "response")

# Match partial content
mock.add_response(r"analyze.*code", "response")

# Match optional words
mock.add_response(r"rewrite( in)? formal", "response")
```

**Default fallback** (catch-all):
```python
mock.set_default_response("Default response for anything unmatched")
```

## Troubleshooting

### Issue: `ValueError: No response configured for prompt`

**Cause**: Mock doesn't have a matching response pattern and no default is set.

**Solution**:
```python
# Option 1: Add specific response
mock.add_response("your prompt", "response")

# Option 2: Add regex pattern
mock.add_response(r"your.*pattern", "response")

# Option 3: Set default
mock.set_default_response("Default response")
```

### Issue: `FileNotFoundError` when loading fixtures

**Cause**: Fixture file doesn't exist or path is wrong.

**Solution**:
```python
# Check the file exists in tests/fixtures/llm/category/name.txt
# Verify category and name are correct
response = load_fixture_response("tov", "rewrite-formal")  # ✅
response = load_fixture_response("tov", "rewrite_formal")  # ❌ Wrong name
```

### Issue: Assertion helpers fail with unclear errors

**Cause**: Pattern doesn't match call history.

**Debug**:
```python
# Check what was actually called
prompts = get_llm_call_prompts(mock)
print(f"Actual prompts: {prompts}")

# Check call count
print(f"Call count: {mock.get_call_count()}")

# Check if pattern matches
if mock.was_called_with(r"your pattern"):
    print("Pattern matched!")
else:
    print("Pattern did not match")
```

### Issue: Tests pass locally but fail in CI

**Cause**: Accidentally making real API calls or relying on environment.

**Solution**:
- Ensure you're using mock fixtures, not real LLM client
- Don't use environment variables for API keys in mock tests
- Verify all LLM calls go through the mock

### Issue: Regex pattern not matching

**Cause**: Regex syntax error or case sensitivity.

**Debug**:
```python
import re

# Test your pattern
pattern = r"your.*pattern"
text = "your actual prompt text"
if re.search(pattern, text, re.IGNORECASE):
    print("✅ Pattern matches!")
else:
    print("❌ Pattern doesn't match")
```

**Common fixes**:
```python
# Escape special characters
mock.add_response(r"what\?", "response")  # Match literal "?"

# Use case-insensitive matching (default in MockLLMClient)
mock.add_response(r"analyze", "response")  # Matches "Analyze", "ANALYZE", etc.

# Make spaces optional
mock.add_response(r"analyze\s+code", "response")  # Match "analyze  code"
```

## Environment Variables

### `RUN_EXAMPLE_TESTS`

Controls whether example tests run.

```bash
# Run example tests
RUN_EXAMPLE_TESTS=1 uv run pytest tests/test_llm_examples.py -v

# Skip example tests (default)
uv run pytest tests/test_llm_examples.py -v
```

### `RUN_INTEGRATION_TESTS`

Controls whether integration tests run (separate from LLM testing).

```bash
# Run integration tests
RUN_INTEGRATION_TESTS=1 uv run pytest -v
```

**Note**: Integration tests make real API calls and should not be run by AI agents or in CI without proper configuration.

## Related Documentation

- [spec-009: LLM Integration Architecture](spec/009-llm-integration.md) - Overall LLM architecture
- [spec-010: LLM Testing Infrastructure](spec/010-llm-testing.md) - Testing infrastructure design
- [lsimons-llm](https://github.com/lsimons-bot/lsimons-llm) - Shared LLM client library
- [AGENTS.md](../AGENTS.md) - Development workflow and guidelines
- [README.md](../README.md) - Project overview and setup

## Summary

The LLM testing infrastructure provides:

1. **MockLLMClient** - Fast, deterministic LLM simulation
2. **Fixtures** - Reusable response templates
3. **Pytest fixtures** - Pre-configured mocks for common scenarios
4. **Assertion helpers** - Easy verification of LLM interactions
5. **Examples** - 19 comprehensive test examples

**Next Steps**:
- Browse `tests/test_llm_examples.py` for patterns to copy
- Create fixtures for your use cases in `tests/fixtures/llm/`
- Use `mock_llm_tov`, `mock_llm_viz`, or `mock_llm_empty` fixtures
- Write tests that verify both responses and call patterns
- Run `RUN_EXAMPLE_TESTS=1 uv run pytest` to see examples in action
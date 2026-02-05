# 009 - LLM Integration Architecture

**Purpose:** Establish foundational LLM integration for AI-powered features like tone-of-voice rewriting and image generation

**Requirements:**
- Use a remote LiteLLM with URL + API key
- Support multiple models
- Configuration via environment variables and config file
- Prompt management system for organizing and versioning prompts
- Basic connectivity testing capability
- Rate limiting and error handling with retries
- Type-safe API with full typing support

**Design Approach:**
- **Single LLM provider**: Depend on external LiteLLM service for provider independence
- **Configuration hierarchy**: Environment variables override config file settings
- **Prompts as code**: Store prompts in `prompts/` directory as `.md` files
- **Fail-fast validation**: Check configuration and connectivity early
- **Shared client library**: Use [lsimons-llm](https://github.com/lsimons-bot/lsimons-llm) for the underlying HTTP client

**Architecture Components:**

### 1. LLM Client
Use the shared `lsimons-llm` library via a thin wrapper class (`quarto4sbp/llm/client.py`) that adds TOML configuration file support.

The wrapper provides a `prompt()` interface that converts single prompts to the messages format expected by the underlying client.

### 2. Configuration System (`quarto4sbp/llm/config.py`)
- Read from `~/.config/q4s.toml` or `q4s.toml` in project root
- Environment variables: `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`
- API provider: LiteLLM
- Default model: `azure/gpt-5-mini`

### 3. Prompt Management (`prompts/` directory)
```
prompts/
  tov/
    system.txt              # System prompt for tone of voice
    rewrite-slide.txt       # Prompt for slide rewriting
  viz/
    analyze-slide.txt       # Prompt for slide analysis
    generate-image.txt      # Prompt for image generation
  common/
    format-json.txt         # Common prompt snippets
```

### 4. Testing Command (`q4s llm test`)
- Verify configuration loaded correctly
- Test API connectivity with simple prompt
- Display token usage and response time
- Validate API key and permissions

**Configuration File Format:**
```toml
[llm]
model = "azure/gpt-5-mini"    # model name
api_key = "${LLM_API_KEY}"    # supports env var expansion
base_url = ""                 # LiteLLM endpoint
max_tokens = 10000            # default max tokens
temperature = 0.7             # default temperature
timeout = 30                  # request timeout in seconds

[llm.retry]
max_attempts = 3              # retry attempts
backoff_factor = 2            # exponential backoff multiplier
```

**Environment Variables:**
- `LLM_API_KEY` - API key (required for cloud providers)
- `LLM_BASE_URL` - Custom API endpoint
- `LLM_MODEL` - Override model selection

**Implementation Notes:**
- Use lsimons-llm for HTTP requests (handles retries, auth, etc.)
- Use `tomli` for TOML parsing (from stdlib in Python 3.11+)
- Store prompts as plain text files, load with `Path.read_text()`
- Support template variables in prompts using Python f-strings or simple `.format()`
- Error messages must be actionable (e.g., "Set LLM_API_KEY environment variable")
- Cache prompt file contents to avoid repeated disk reads

**Security Considerations:**
- Never log API keys
- Validate and sanitize user input before sending to LLM
- Set reasonable token limits to prevent cost overruns

**Testing Strategy:**
- Unit tests with mocked responses (no real API calls)
- Mock client for testing LLM-dependent features (see spec-010)
- Integration tests gated by `RUN_INTEGRATION_TESTS=1` (optional, uses real APIs)
- Test configuration loading from files and environment
- Test error handling (network errors, invalid API keys, rate limits)

**Status:** Implemented

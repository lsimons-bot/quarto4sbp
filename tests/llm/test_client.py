"""Tests for LLM client."""

import unittest
from unittest.mock import MagicMock, patch

from quarto4sbp.llm.client import LLMClient, create_client
from quarto4sbp.llm.config import LLMConfig


class TestLLMClientInitialization(unittest.TestCase):
    """Test cases for LLM client initialization."""

    @patch("quarto4sbp.llm.client.load_config")
    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_init_without_config(
        self, mock_base_client: MagicMock, mock_load_config: MagicMock
    ) -> None:
        """Test initialization without explicit config loads from system."""
        mock_config = LLMConfig(
            model="test-model",
            api_key="test-key",
        )
        mock_load_config.return_value = mock_config

        client = LLMClient()

        self.assertEqual(client.config, mock_config)
        mock_load_config.assert_called_once()
        mock_base_client.assert_called_once()

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_init_with_config(self, mock_base_client: MagicMock) -> None:
        """Test initialization with explicit config."""
        config = LLMConfig(
            model="test-model",
            api_key="test-key",
        )

        client = LLMClient(config)

        self.assertEqual(client.config, config)
        mock_base_client.assert_called_once()


class TestLLMClientPrompt(unittest.TestCase):
    """Test cases for LLM client prompt method."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = LLMConfig(
            model="test-model",
            api_key="test-key",
            temperature=0.7,
            max_tokens=1000,
            timeout=30,
            max_attempts=3,
            backoff_factor=2,
        )

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_prompt_basic(self, mock_base_client_class: MagicMock) -> None:
        """Test basic prompt call."""
        mock_client = MagicMock()
        mock_client.chat.return_value = "Test response"
        mock_base_client_class.return_value = mock_client

        client = LLMClient(self.config)
        response = client.prompt("Test prompt")

        self.assertEqual(response, "Test response")
        mock_client.chat.assert_called_once()
        # Verify messages format
        call_args = mock_client.chat.call_args
        messages = call_args[0][0]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "Test prompt")

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_prompt_with_system_message(self, mock_base_client_class: MagicMock) -> None:
        """Test prompt with system message."""
        mock_client = MagicMock()
        mock_client.chat.return_value = "Test response"
        mock_base_client_class.return_value = mock_client

        client = LLMClient(self.config)
        response = client.prompt("Test prompt", system="System message")

        self.assertEqual(response, "Test response")
        # Verify messages include system message
        call_args = mock_client.chat.call_args
        messages = call_args[0][0]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "System message")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "Test prompt")

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_prompt_with_overrides(self, mock_base_client_class: MagicMock) -> None:
        """Test prompt with parameter overrides."""
        mock_client = MagicMock()
        mock_client.chat.return_value = "Test response"
        mock_base_client_class.return_value = mock_client

        client = LLMClient(self.config)
        response = client.prompt(
            "Test prompt",
            model="different-model",
            temperature=0.5,
            max_tokens=500,
        )

        self.assertEqual(response, "Test response")
        # Verify overrides were passed
        call_args = mock_client.chat.call_args
        self.assertEqual(call_args[1]["model"], "different-model")
        self.assertEqual(call_args[1]["temperature"], 0.5)
        self.assertEqual(call_args[1]["max_tokens"], 500)

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_prompt_failure_raises_value_error(
        self, mock_base_client_class: MagicMock
    ) -> None:
        """Test that prompt raises ValueError on failure."""
        mock_client = MagicMock()
        mock_client.chat.side_effect = Exception("API error")
        mock_base_client_class.return_value = mock_client

        client = LLMClient(self.config)

        with self.assertRaises(ValueError) as context:
            client.prompt("Test prompt")

        self.assertIn("LLM API call failed", str(context.exception))
        self.assertIn("API error", str(context.exception))


class TestLLMClientTestConnectivity(unittest.TestCase):
    """Test cases for LLM client connectivity testing."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = LLMConfig(
            model="test-model",
            api_key="test-key",
        )

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_connectivity_success(self, mock_base_client_class: MagicMock) -> None:
        """Test successful connectivity test."""
        mock_client = MagicMock()
        mock_client.chat.return_value = "Hello from LLM"
        mock_base_client_class.return_value = mock_client

        client = LLMClient(self.config)
        result = client.test_connectivity()

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["response"])
        self.assertIsNone(result["error"])
        self.assertGreater(result["elapsed_time"], 0)
        self.assertEqual(result["model"], "test-model")

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_connectivity_failure(self, mock_base_client_class: MagicMock) -> None:
        """Test failed connectivity test."""
        mock_client = MagicMock()
        mock_client.chat.side_effect = Exception("Connection failed")
        mock_base_client_class.return_value = mock_client

        client = LLMClient(self.config)
        result = client.test_connectivity()

        self.assertFalse(result["success"])
        self.assertIsNone(result["response"])
        self.assertIsNotNone(result["error"])
        self.assertIn("Connection failed", str(result["error"]))
        self.assertGreater(result["elapsed_time"], 0)
        self.assertEqual(result["model"], "test-model")


class TestLLMClientContextManager(unittest.TestCase):
    """Test cases for LLM client context manager."""

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_context_manager(self, mock_base_client_class: MagicMock) -> None:
        """Test client can be used as context manager."""
        mock_client = MagicMock()
        mock_base_client_class.return_value = mock_client

        config = LLMConfig(model="test-model", api_key="test-key")

        with LLMClient(config) as client:
            self.assertIsInstance(client, LLMClient)

        mock_client.close.assert_called_once()


class TestCreateClient(unittest.TestCase):
    """Test cases for create_client convenience function."""

    @patch("quarto4sbp.llm.client.load_config")
    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_create_client_without_config(
        self, mock_base_client: MagicMock, mock_load_config: MagicMock
    ) -> None:
        """Test creating client without config."""
        mock_config = LLMConfig(
            model="test-model",
            api_key="test-key",
        )
        mock_load_config.return_value = mock_config

        client = create_client()

        self.assertIsInstance(client, LLMClient)
        self.assertEqual(client.config, mock_config)

    @patch("quarto4sbp.llm.client.BaseLLMClient")
    def test_create_client_with_config(self, mock_base_client: MagicMock) -> None:
        """Test creating client with config."""
        config = LLMConfig(
            model="test-model",
            api_key="test-key",
        )

        client = create_client(config)

        self.assertIsInstance(client, LLMClient)
        self.assertEqual(client.config, config)


if __name__ == "__main__":
    unittest.main()

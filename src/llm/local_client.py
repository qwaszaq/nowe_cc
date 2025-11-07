"""
Local LLM Client for LM Studio Server

Connects to LM Studio server running openai/gpt-oss-20b at 192.168.200.226
Provides OpenAI-compatible API interface for all Destiny agents.
"""

import requests
import json
import time
from typing import List, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class LocalLLMClient:
    """
    Client for local LM Studio server running openai/gpt-oss-20b

    Server: 192.168.200.226:1234
    Model: openai/gpt-oss-20b
    API: OpenAI-compatible
    """

    def __init__(
        self,
        base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "openai/gpt-oss-20b",
        timeout: int = 120
    ):
        """
        Initialize local LLM client

        Args:
            base_url: LM Studio server URL
            model: Model name (openai/gpt-oss-20b)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

        # Verify connection on initialization
        self._verify_connection()

    def _verify_connection(self):
        """Verify LM Studio server is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                timeout=5
            )
            response.raise_for_status()
            logger.info(f"✅ Connected to LM Studio at {self.base_url}")
            logger.info(f"✅ Model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to LM Studio: {e}")
            logger.error(f"   Make sure LM Studio is running at {self.base_url}")
            logger.error(f"   Make sure model '{self.model}' is loaded")
            raise ConnectionError(
                f"Cannot connect to LM Studio at {self.base_url}. "
                f"Error: {e}"
            )

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        stop: Optional[List[str]] = None
    ) -> str:
        """
        Send chat completion request to local LLM

        Args:
            system_prompt: Agent personality and role definition
            user_message: The task/question from user
            context: Previous conversation history (optional)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum response length
            stop: Stop sequences

        Returns:
            LLM response text

        Example:
            >>> client = LocalLLMClient()
            >>> response = client.chat(
            ...     system_prompt="You are a financial analyst",
            ...     user_message="Analyze this balance sheet: ..."
            ... )
        """
        # Build messages array
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation context if provided
        if context:
            messages.extend(context)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        if stop:
            payload["stop"] = stop

        # Send request
        start_time = time.time()

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            # Parse response
            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Log metrics
            elapsed = time.time() - start_time
            usage = result.get("usage", {})
            logger.info(
                f"LLM response: {elapsed:.2f}s, "
                f"{usage.get('total_tokens', 0)} tokens"
            )

            return content

        except requests.exceptions.Timeout:
            logger.error(f"LLM request timeout after {self.timeout}s")
            raise TimeoutError(
                f"LLM request timeout after {self.timeout}s. "
                f"Consider increasing timeout or simplifying prompt."
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"LLM request failed: {e}")
            raise RuntimeError(f"LLM request failed: {e}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.error(f"Raw response: {response.text if 'response' in locals() else 'N/A'}")
            raise ValueError(f"Invalid LLM response format: {e}")

    def chat_streaming(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ):
        """
        Stream chat completion response (for long outputs)

        Yields response chunks as they arrive.

        Example:
            >>> for chunk in client.chat_streaming(system_prompt, user_message):
            ...     print(chunk, end='', flush=True)
        """
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": user_message})

        # Prepare streaming request
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()

            # Stream chunks
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: ' prefix
                        if data_str == '[DONE]':
                            break
                        try:
                            chunk_data = json.loads(data_str)
                            delta = chunk_data['choices'][0]['delta']
                            if 'content' in delta:
                                yield delta['content']
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text

        Note: This is a rough estimate. Actual tokenization may differ.
        Rule of thumb: 1 token ≈ 4 characters for English text
        """
        return len(text) // 4

    def health_check(self) -> Dict:
        """
        Check LM Studio server health

        Returns:
            {
                'status': 'healthy',
                'model': 'openai/gpt-oss-20b',
                'server': '192.168.200.226:1234',
                'latency_ms': 45
            }
        """
        start = time.time()

        try:
            # Quick test request
            response = self.chat(
                system_prompt="You are a test assistant.",
                user_message="Reply with 'OK'",
                max_tokens=10
            )

            latency_ms = int((time.time() - start) * 1000)

            return {
                'status': 'healthy',
                'model': self.model,
                'server': self.base_url,
                'latency_ms': latency_ms,
                'test_response': response
            }

        except Exception as e:
            return {
                'status': 'unhealthy',
                'model': self.model,
                'server': self.base_url,
                'error': str(e)
            }


# Singleton instance for shared use
_client_instance = None

def get_llm_client() -> LocalLLMClient:
    """
    Get singleton LLM client instance

    Returns:
        Shared LocalLLMClient instance
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = LocalLLMClient()
    return _client_instance

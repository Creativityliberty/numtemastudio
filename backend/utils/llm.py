"""
Client LLM Unifié pour Nümtema Agents Studio

Abstraction simple pour interagir avec différents fournisseurs LLM
sans dépendance à des frameworks lourds.
"""

import os
from typing import Optional, Generator, Dict, Any, List
from functools import lru_cache
from abc import ABC, abstractmethod

from models import LLMProvider


class BaseLLMClient(ABC):
    """Interface de base pour les clients LLM"""
    
    @abstractmethod
    def call(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        pass
    
    @abstractmethod
    def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        pass


class OpenAIClient(BaseLLMClient):
    """Client OpenAI"""
    
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.default_model = "gpt-4o"
    
    def call(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        stream = self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class AnthropicClient(BaseLLMClient):
    """Client Anthropic"""
    
    def __init__(self):
        from anthropic import Anthropic
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.default_model = "claude-sonnet-4-20250514"
    
    def call(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        kwargs = {
            "model": model or self.default_model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        kwargs = {
            "model": model or self.default_model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        
        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text


class GoogleClient(BaseLLMClient):
    """Client Google (Gemini)"""
    
    def __init__(self):
        from google import genai
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.default_model = "gemini-2.5-pro"
    
    def call(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = self.client.models.generate_content(
            model=model or self.default_model,
            contents=full_prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )
        return response.text
    
    def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        for chunk in self.client.models.generate_content_stream(
            model=model or self.default_model,
            contents=full_prompt
        ):
            if chunk.text:
                yield chunk.text


class OllamaClient(BaseLLMClient):
    """Client Ollama (local)"""
    
    def __init__(self):
        import httpx
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = httpx.Client(timeout=120.0)
        self.default_model = "llama3"
    
    def call(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        if system_prompt:
            payload["system"] = system_prompt
        
        response = self.client.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        response.raise_for_status()
        return response.json()["response"]
    
    def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": True
        }
        if system_prompt:
            payload["system"] = system_prompt
        
        with self.client.stream(
            "POST",
            f"{self.base_url}/api/generate",
            json=payload
        ) as response:
            for line in response.iter_lines():
                import json
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]


class LLMClient:
    """Client LLM unifié avec routing automatique"""
    
    _clients: Dict[LLMProvider, BaseLLMClient] = {}
    
    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI):
        self.provider = provider
        self._ensure_client(provider)
    
    def _ensure_client(self, provider: LLMProvider) -> BaseLLMClient:
        if provider not in self._clients:
            if provider == LLMProvider.OPENAI:
                self._clients[provider] = OpenAIClient()
            elif provider == LLMProvider.ANTHROPIC:
                self._clients[provider] = AnthropicClient()
            elif provider == LLMProvider.GOOGLE:
                self._clients[provider] = GoogleClient()
            elif provider == LLMProvider.OLLAMA:
                self._clients[provider] = OllamaClient()
            else:
                raise ValueError(f"Provider inconnu: {provider}")
        return self._clients[provider]
    
    @property
    def client(self) -> BaseLLMClient:
        return self._ensure_client(self.provider)
    
    def call(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        return self.client.call(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt
        )
    
    def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        yield from self.client.stream(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt
        )
    
    @lru_cache(maxsize=1000)
    def call_cached(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """Version cachée pour économiser les tokens"""
        return self.call(prompt, model, system_prompt=system_prompt)


# Singleton global
_default_provider = LLMProvider(os.getenv("LLM_PROVIDER", "openai"))
llm_client = LLMClient(_default_provider)


def call_llm(
    prompt: str,
    model: Optional[str] = None,
    provider: Optional[LLMProvider] = None,
    **kwargs
) -> str:
    """Fonction utilitaire globale"""
    if provider and provider != llm_client.provider:
        client = LLMClient(provider)
        return client.call(prompt, model, **kwargs)
    return llm_client.call(prompt, model, **kwargs)


def stream_llm(
    prompt: str,
    model: Optional[str] = None,
    provider: Optional[LLMProvider] = None,
    **kwargs
) -> Generator[str, None, None]:
    """Fonction utilitaire globale avec streaming"""
    if provider and provider != llm_client.provider:
        client = LLMClient(provider)
        yield from client.stream(prompt, model, **kwargs)
    else:
        yield from llm_client.stream(prompt, model, **kwargs)


__all__ = [
    "LLMClient",
    "BaseLLMClient",
    "OpenAIClient",
    "AnthropicClient",
    "GoogleClient",
    "OllamaClient",
    "call_llm",
    "stream_llm",
    "llm_client",
]

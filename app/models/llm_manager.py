"""
LLM Manager - Handles interaction with Ollama models
Supports both Mistral 7B and Llama 3.1 8B
"""

import sys
from pathlib import Path
from typing import Optional, Dict
import subprocess
import json

sys.path.append(str(Path(__file__).parent.parent))
from config import LLM_CONFIG


class OllamaManager:
    """Manages Ollama LLM interactions"""

    def __init__(self):
        self.config = LLM_CONFIG
        self.current_model = None

    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def list_available_models(self) -> list:
        """List models available in Ollama"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Parse output
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = [line.split()[0] for line in lines if line.strip()]
                return models
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def generate(self, prompt: str, model_name: str = None,
                temperature: float = None, max_tokens: int = None) -> Optional[str]:
        """
        Generate text using Ollama

        Args:
            prompt: The input prompt
            model_name: Model to use (default: mistral)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None if error
        """
        # Use defaults from config if not specified
        if model_name is None:
            model_name = self.config['mistral']['model_name']

        if temperature is None:
            # Get temperature from config based on model
            if 'mistral' in model_name.lower():
                temperature = self.config['mistral']['temperature']
            else:
                temperature = self.config['llama']['temperature']

        if max_tokens is None:
            if 'mistral' in model_name.lower():
                max_tokens = self.config['mistral']['max_tokens']
            else:
                max_tokens = self.config['llama']['max_tokens']

        try:
            # Build Ollama command
            cmd_input = {
                "model": model_name,
                "prompt": prompt,
                "temperature": temperature,
                "num_predict": max_tokens,
                "stream": False
            }

            # Call Ollama API via subprocess
            result = subprocess.run(
                ['ollama', 'run', model_name, '--format', 'json'],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # Ollama in non-streaming mode returns the generated text directly
                return result.stdout.strip()
            else:
                print(f"Error from Ollama: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("Request to Ollama timed out")
            return None
        except Exception as e:
            print(f"Error generating text: {e}")
            return None

    def generate_conversation_response(self, prompt: str,
                                     use_mistral: bool = True) -> Optional[str]:
        """
        Generate a conversation response
        Uses Mistral for quick conversational responses

        Args:
            prompt: Conversation prompt
            use_mistral: Whether to use Mistral (True) or Llama (False)

        Returns:
            Generated response text
        """
        model_name = self.config['mistral']['model_name'] if use_mistral else self.config['llama']['model_name']
        return self.generate(prompt, model_name=model_name)

    def generate_correction(self, user_text: str, context: str = "") -> Optional[Dict]:
        """
        Generate grammar/vocabulary correction
        Uses Llama for more detailed analysis

        Args:
            user_text: User's German text
            context: Additional context

        Returns:
            Dict with correction and explanation
        """
        prompt = f"""You are a German language teacher. Analyze this German text and provide corrections if needed.

Student's text: "{user_text}"
Context: {context if context else "General conversation"}

Provide your response in this exact format:
CORRECT: [yes/no]
CORRECTED_TEXT: [the corrected version, or same as original if correct]
EXPLANATION: [brief explanation of the mistake, or praise if correct]

Be encouraging and patient."""

        response = self.generate(
            prompt,
            model_name=self.config['llama']['model_name'],
            temperature=0.3  # Lower temperature for more consistent corrections
        )

        if not response:
            return None

        # Parse response
        try:
            lines = response.strip().split('\n')
            correction_dict = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    correction_dict[key.strip()] = value.strip()

            return {
                'is_correct': correction_dict.get('CORRECT', 'yes').lower() == 'yes',
                'corrected_text': correction_dict.get('CORRECTED_TEXT', user_text),
                'explanation': correction_dict.get('EXPLANATION', '')
            }
        except Exception as e:
            print(f"Error parsing correction: {e}")
            return None


# Fallback for when Ollama is not available
class MockLLM:
    """Mock LLM for testing without Ollama"""

    def __init__(self):
        self.responses = {
            "greeting": "Hallo! Ich heiße Otto. Wie geht es dir?",
            "default": "Ja, das verstehe ich. Können Sie mehr sagen?"
        }

    def check_ollama_installed(self) -> bool:
        return False

    def generate(self, prompt: str, **kwargs) -> str:
        """Return a mock response"""
        if "Wie heißt" in prompt:
            return "Ich heiße Otto! Und du? Wie heißt du?"
        elif "möchten" in prompt or "trinken" in prompt:
            return "Natürlich! Möchten Sie Kaffee oder Tee?"
        else:
            return "Interessant! Erzähl mir mehr darüber."

    def generate_conversation_response(self, prompt: str, **kwargs) -> str:
        return self.generate(prompt)

    def generate_correction(self, user_text: str, context: str = "") -> Dict:
        return {
            'is_correct': True,
            'corrected_text': user_text,
            'explanation': 'Sehr gut! Das ist richtig.'
        }


# Singleton instance
_llm_manager = None


def get_llm() -> OllamaManager:
    """Get LLM manager singleton (Ollama or Mock)"""
    global _llm_manager
    if _llm_manager is None:
        # Try to use Ollama, fallback to mock
        ollama = OllamaManager()
        if ollama.check_ollama_installed():
            print("✓ Ollama detected - using real LLM")
            _llm_manager = ollama
        else:
            print("⚠ Ollama not detected - using mock responses")
            print("  Install Ollama from: https://ollama.ai")
            _llm_manager = MockLLM()
    return _llm_manager

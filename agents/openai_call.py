"""Utility wrappers for model-specific OpenAI text calls."""

from __future__ import annotations

from openai import OpenAI


def generate_text(client: OpenAI, model: str, message: str) -> str:
    """Generate text using model-appropriate API surface.

    GPT-4.1 family works reliably through Chat Completions.
    GPT-5 family and others can use Responses API.
    """
    if model.startswith("gpt-4.1"):
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
        )
        return completion.choices[0].message.content or ""

    completion = client.responses.create(model=model, input=message)
    return completion.output_text or ""

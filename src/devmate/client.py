
from __future__ import annotations

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_BASE_MODEL = "Qwen/Qwen3-0.6B"
DEFAULT_ADAPTER_MODEL = "Pranesh0805-S/DevMate-V3"


class DevMate:
    """Load the DevMate LoRA adapter and generate text."""

    def __init__(
        self,
        base_model: str = DEFAULT_BASE_MODEL,
        adapter_model: str = DEFAULT_ADAPTER_MODEL,
        device: str | None = None,
        max_new_tokens: int = 180,
    ) -> None:
        if max_new_tokens < 1:
            raise ValueError("max_new_tokens must be at least 1.")

        self.max_new_tokens = max_new_tokens
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(adapter_model)

        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            dtype=torch.float32,
            low_cpu_mem_usage=True,
        )

        self.model = PeftModel.from_pretrained(base, adapter_model)
        self.model.to(self.device)
        self.model.eval()

    def generate(self, prompt: str) -> str:
        """Generate a response to a text prompt."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string.")

        messages = [{"role": "user", "content": prompt}]
        formatted = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )

        inputs = self.tokenizer(formatted, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
            )

        generated = outputs[0, inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(
            generated,
            skip_special_tokens=True,
        ).strip()

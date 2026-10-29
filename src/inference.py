
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_MODEL = "Qwen/Qwen3-0.6B"
ADAPTER_MODEL = "Pranesh0805-S/DevMate-V3"


def main():
    print(f"Loading tokenizer from {ADAPTER_MODEL}...")
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_MODEL)

    print(f"Loading base model: {BASE_MODEL}...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )

    print("Loading DevMate V3 adapter...")
    model = PeftModel.from_pretrained(model, ADAPTER_MODEL)
    model.eval()

    prompt = (
        "Explain what a Python function is in simple terms. "
        "Give one short code example."
    )
    messages = [{"role": "user", "content": prompt}]

    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )

    inputs = tokenizer(formatted_prompt, return_tensors="pt")

    print("\nGenerating DevMate V3 response...\n")
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=180,
            do_sample=False,
        )

    new_tokens = outputs[0, inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(new_tokens, skip_special_tokens=True)

    print("=== DevMate V3 Response ===")
    print(answer)


if __name__ == "__main__":
    main()

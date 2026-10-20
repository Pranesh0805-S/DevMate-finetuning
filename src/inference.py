
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-0.6B"


def main():
    print(f"Loading model: {MODEL_NAME}")
    print("The first run downloads model files. Please wait...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
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

    print("\nGenerating response...\n")

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
        )

    new_tokens = outputs[0, inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True,
    )

    print("=== DevMate Baseline Response ===")
    print(answer)


if __name__ == "__main__":
    main()

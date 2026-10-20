
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-0.6B"
ADAPTER_DIR = "results/devmate-lora"

PROMPTS = [
    "Explain Python dictionaries with a short code example.",
    "What is the difference between git fetch and git pull?",
    "Explain how to debug a Python TypeError.",
]


def generate_answer(model, tokenizer, question):
    messages = [{"role": "user", "content": question}]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors="pt",
        return_dict=True,
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=160,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading original model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    base_model.eval()

    for question in PROMPTS:
        print("\n" + "=" * 70)
        print("QUESTION:", question)
        print("\n[BASE MODEL]")
        print(generate_answer(base_model, tokenizer, question))

    del base_model
    print("\nLoading fine-tuned DevMate...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(base_model, ADAPTER_DIR)
    model.eval()

    for question in PROMPTS:
        print("\n" + "=" * 70)
        print("QUESTION:", question)
        print("\n[FINETUNED DEVMATE]")
        print(generate_answer(model, tokenizer, question))


if __name__ == "__main__":
    main()

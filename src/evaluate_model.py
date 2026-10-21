
import gc
import json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-0.6B"
EVAL_FILE = Path("data/eval.jsonl")
OUTPUT_FILE = Path("results/model-comparison-v3.jsonl")

ADAPTERS = {
    "DEVMATE V1": Path("results/devmate-lora"),
    "DEVMATE V2": Path("results/devmate-lora-v2"),
    "DEVMATE V3": Path("results/devmate-lora-v3"),
}

MAX_NEW_TOKENS = 256


def load_questions():
    questions = []

    with EVAL_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            example = json.loads(line)
            messages = example["messages"]

            user_messages = [
                message["content"]
                for message in messages
                if message["role"] == "user"
            ]

            if not user_messages:
                raise ValueError(
                    f"No user message on line {line_number}"
                )

            questions.append(user_messages[0])

    if not questions:
        raise ValueError("Evaluation dataset is empty.")

    return questions


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

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        new_tokens,
        skip_special_tokens=True,
    ).strip()


def load_base_model():
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()
    return model


def evaluate_variant(label, tokenizer, questions, adapter_dir=None):
    print(f"\nEvaluating {label} ({len(questions)} questions)")

    base_model = load_base_model()

    if adapter_dir is not None:
        model = PeftModel.from_pretrained(
            base_model,
            str(adapter_dir),
        )
        model.eval()
    else:
        model = base_model

    results = []

    try:
        for index, question in enumerate(questions, start=1):
            print(f"  Question {index}/{len(questions)}")

            answer = generate_answer(model, tokenizer, question)

            results.append({
                "question": question,
                "answer": answer,
            })
    finally:
        del model
        if adapter_dir is not None:
            del base_model
        gc.collect()

    return results


def main():
    if not EVAL_FILE.exists():
        raise FileNotFoundError(EVAL_FILE)

    for adapter_dir in ADAPTERS.values():
        if not adapter_dir.exists():
            raise FileNotFoundError(
                f"Adapter not found: {adapter_dir}"
            )

    questions = load_questions()
    print(f"Loaded {len(questions)} evaluation questions.")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    all_results = {}

    variants = [("BASE MODEL", None)]
    variants.extend(ADAPTERS.items())

    for label, adapter_dir in variants:
        variant_results = evaluate_variant(
            label,
            tokenizer,
            questions,
            adapter_dir,
        )

        all_results[label] = variant_results

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for index, question in enumerate(questions):
            record = {"question": question}

            for label, _ in variants:
                record[label] = all_results[label][index]["answer"]

            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    print(f"\nEvaluation complete: {len(questions)} questions")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()


import json
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "Qwen/Qwen3-0.6B"
TRAIN_FILE = Path("data/train.jsonl")
EVAL_FILE = Path("data/eval.jsonl")
OUTPUT_DIR = Path("results/devmate-lora-v3")
MAX_LENGTH = 256


def load_examples(path):
    examples = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON in {path}, line {line_number}"
                ) from error

            messages = item.get("messages")
            if (
                not isinstance(messages, list)
                or len(messages) < 2
                or messages[-1].get("role") != "assistant"
            ):
                raise ValueError(
                    f"{path}, line {line_number}: expected messages "
                    "ending with an assistant response"
                )

            examples.append(messages)

    if not examples:
        raise ValueError(f"No examples found in {path}")

    return examples


def prepare_features(examples, tokenizer):
    features = []

    for messages in examples:
        prompt = tokenizer.apply_chat_template(
            messages[:-1],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )

        full_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
            enable_thinking=False,
        )

        prompt_ids = tokenizer(
            prompt, add_special_tokens=False
        )["input_ids"]

        full_ids = tokenizer(
            full_text,
            add_special_tokens=False,
            truncation=True,
            max_length=MAX_LENGTH,
        )["input_ids"]

        # Only calculate loss on assistant response tokens.
        prompt_length = min(len(prompt_ids), len(full_ids))
        labels = full_ids.copy()
        labels[:prompt_length] = [-100] * prompt_length

        if not any(token != -100 for token in labels):
            raise ValueError(
                "No assistant tokens remain after truncation. "
                "Shorten the example or increase MAX_LENGTH."
            )

        features.append({
            "input_ids": full_ids,
            "labels": labels,
        })

    return features


class CausalDataset(torch.utils.data.Dataset):
    def __init__(self, features):
        self.features = features

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        return self.features[index]


def make_collator(tokenizer):
    def collate(batch):
        max_len = max(len(item["input_ids"]) for item in batch)
        input_ids, labels, attention_mask = [], [], []

        for item in batch:
            pad_len = max_len - len(item["input_ids"])

            input_ids.append(
                item["input_ids"]
                + [tokenizer.pad_token_id] * pad_len
            )
            labels.append(item["labels"] + [-100] * pad_len)
            attention_mask.append(
                [1] * len(item["input_ids"]) + [0] * pad_len
            )

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
            "attention_mask": torch.tensor(
                attention_mask, dtype=torch.long
            ),
        }

    return collate


def main():
    for path in (TRAIN_FILE, EVAL_FILE):
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset: {path}")

    train_examples = load_examples(TRAIN_FILE)
    eval_examples = load_examples(EVAL_FILE)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Preparing training and evaluation datasets...")
    train_features = prepare_features(train_examples, tokenizer)
    eval_features = prepare_features(eval_examples, tokenizer)

    print("Loading base model on CPU...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.config.use_cache = False
    model.config.pad_token_id = tokenizer.pad_token_id

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        use_cpu=True,
        num_train_epochs=2,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=1e-4,
        logging_steps=1,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none",
        dataloader_pin_memory=False,
        optim="adamw_torch",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=CausalDataset(train_features),
        eval_dataset=CausalDataset(eval_features),
        data_collator=make_collator(tokenizer),
    )

    print(
        f"Starting CPU LoRA training: "
        f"{len(train_features)} train / {len(eval_features)} eval examples"
    )

    trainer.train()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print(f"LoRA adapter saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

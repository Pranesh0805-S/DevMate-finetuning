---
base_model: Qwen/Qwen3-0.6B
library_name: peft
pipeline_tag: text-generation
tags:
  - qwen3
  - lora
  - peft
  - small-language-model
  - developer-tools
  - experimental
---

# DevMate V3 — Small Language Model Fine-Tuning

**An experimental developer-focused language model adapter fine-tuned with LoRA on Qwen3-0.6B.**

DevMate V3 explores how targeted training examples influence a small language model's responses to programming questions and developer workflows. It uses Parameter-Efficient Fine-Tuning (PEFT) with Low-Rank Adaptation (LoRA).

> **Status:** Experimental research project. Results are preliminary and do not establish general improvements across tasks or domains.

## Model Details

- **Model:** DevMate V3
- **Base model:** [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)
- **Fine-tuning method:** LoRA
- **Task:** Text generation
- **Framework:** Hugging Face Transformers and PEFT
- **LoRA rank:** 8
- **LoRA alpha:** 16
- **LoRA dropout:** 0.05
- **Target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`
- **Intended audience:** Developers, students, and researchers exploring small language models

## Intended Uses

DevMate V3 is intended for experimentation with developer-oriented prompts, programming assistance, educational demonstrations, and research into parameter-efficient fine-tuning.

Review and test generated answers before using them in real development workflows.

## Limitations and Risks

- The adapter may generate incorrect, incomplete, or misleading responses.
- Performance may vary across programming languages, prompts, and tasks.
- Fine-tuning does not guarantee improvements over the base model.
- Generated code should be reviewed, executed safely, and checked for security issues.
- The model should not replace authoritative documentation or expert review.
- Evaluation was conducted on a limited set of 21 questions per model; the results may not generalize to real-world usage.

## Loading the Adapter

Install the required libraries:

```bash
pip install torch transformers peft accelerate
```

Load the base model and DevMate V3 adapter:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_id = "Qwen/Qwen3-0.6B"
adapter_id = "Pranesh0805-S/DevMate-V3"

tokenizer = AutoTokenizer.from_pretrained(adapter_id)

base_model = AutoModelForCausalLM.from_pretrained(base_model_id)
model = PeftModel.from_pretrained(base_model, adapter_id)
model.eval()

messages = [
    {
        "role": "user",
        "content": "Explain a Python function with a simple example."
    }
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False,
)

inputs = tokenizer(prompt, return_tensors="pt")

import torch

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        do_sample=False,
    )

new_tokens = outputs[0, inputs["input_ids"].shape[1]:]
print(tokenizer.decode(new_tokens, skip_special_tokens=True))
```

This example demonstrates loading and basic text generation. Hardware requirements and generation behavior depend on the environment. The base model must also be accessible under its own terms.

## Training Details

DevMate V3 was developed using parameter-efficient fine-tuning. The project repository includes training configurations, evaluation scripts, model comparisons, and evaluation review artifacts.

The verified training configuration includes:

- **Base model:** `Qwen/Qwen3-0.6B`
- **LoRA rank:** 8
- **LoRA alpha:** 16
- **LoRA dropout:** 0.05
- **Target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`
- **Epochs:** 2
- **Learning rate:** `1e-4`
- **Training environment:** CPU-based training

Further details about dataset composition, preprocessing, and training-data permissions should be documented when verified.

## Evaluation

Four model variants were evaluated using 21 answers per model.

| Metric | Base Model | DevMate V1 | DevMate V2 | DevMate V3 |
|---|---:|---:|---:|---:|
| Answers evaluated | 21 | 21 | 21 | 21 |
| Correctness rating | 67 | 76 | 79 | 80 |
| Relevance rating | 100 | 99 | 90 | 90 |
| Usefulness rating | 67 | 74 | 58 | 61 |
| Critical errors | 11 | 7 | 4 | 2 |
| Overall score | 74.29% | 79.05% | 72.06% | 73.33% |

### Results Interpretation

In this evaluation, DevMate V3 achieved the highest correctness rating and the fewest critical errors among the four variants. However, its relevance and usefulness ratings were lower than those of the base model.

DevMate V3's overall score was 73.33%, compared with 74.29% for the base model. DevMate V1 achieved the highest overall score at 79.05%.

These findings indicate mixed outcomes rather than a consistent improvement across all metrics.

### Evaluation Limitations

- The evaluation included 21 answers per model.
- The reported rating scales and aggregation procedures should be documented alongside the evaluation methodology.
- The results may not generalize to other prompts, programming tasks, or real-world usage.
- A larger, independently selected evaluation set is needed to assess the reliability of these findings.
- Automatic diagnostics such as response completion and average word count are not measures of factual correctness.

## Licensing

The base model has its own licensing terms. Before redistributing this adapter, verify the base model's license, the permissions associated with the training data, and the license intended for DevMate-specific work.

The license for the DevMate adapter has not been declared here. Do not assume that the base model's license automatically resolves all dataset or adapter redistribution questions.

## Acknowledgements

DevMate was developed as a learning and experimentation project focused on small language models, LoRA fine-tuning, and model evaluation.
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

# DevMate V3 — Small LLM Fine-Tuning

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
- **Intended audience:** Developers, students, and researchers exploring small language models

## Intended Uses

DevMate V3 is intended for experimentation with developer-oriented prompts, programming assistance, and model evaluation.

Potential uses include educational demonstrations, local inference experiments, and research into parameter-efficient fine-tuning. Its responses should be reviewed before being used in real development workflows.

## Limitations and Risks

- The adapter may generate incorrect, incomplete, or misleading responses.
- Performance may vary across programming languages, prompts, and tasks.
- Fine-tuning does not guarantee improvements over the base model.
- Generated code should be reviewed, tested, and checked for security issues.
- The model should not replace authoritative documentation or expert review.

## Loading the Adapter

Install the required libraries:

```bash
pip install torch transformers peft accelerate
```

Load the base model and the published adapter:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_id = "Qwen/Qwen3-0.6B"
adapter_id = "YOUR_HUGGINGFACE_USERNAME/DevMate-V3"

tokenizer = AutoTokenizer.from_pretrained(base_model_id)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id
)

model = PeftModel.from_pretrained(
    base_model,
    adapter_id
)

model.eval()
```

Replace `YOUR_HUGGINGFACE_USERNAME/DevMate-V3` with the actual model repository ID after publication.

This example demonstrates adapter loading. Generation settings and hardware requirements depend on the environment. The loading procedure should be tested before release.

## Training Details

DevMate V3 was developed using parameter-efficient fine-tuning. The project repository includes training configurations, evaluation scripts, model comparisons, and evaluation review artifacts.

The adapter configuration specifies the following:

- **Base model:** Qwen/Qwen3-0.6B
- **LoRA rank:** 8
- **LoRA alpha:** 16
- **LoRA dropout:** 0.05
- **Target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`

Further details about the training dataset, preprocessing, and training hyperparameters should be documented when verified.

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

The overall score for DevMate V3 was 73.33%, compared with 74.29% for the base model. DevMate V1 achieved the highest overall score at 79.05%.

These results indicate mixed outcomes rather than a consistent improvement across every evaluation metric.

### Evaluation Limitations

- The evaluation included 21 answers per model.
- The rating scales and aggregation procedures should be documented alongside the evaluation methodology.
- The results may not generalize to other prompts, programming tasks, or real-world usage.
- A larger, independently selected evaluation set is needed to assess the reliability of these findings.

## Licensing

The base model has its own licensing terms. Before redistributing this adapter, verify the base model's licence, the permissions associated with the training data, and the licence you intend to apply to your own work.

The licence for the DevMate-specific adapter should be explicitly established before public release.

## Acknowledgements

DevMate was developed as a learning and experimentation project focused on small language models, LoRA fine-tuning, and model evaluation.
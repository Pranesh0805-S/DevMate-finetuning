# DevMate — Baseline and Fine-Tuning Evaluation

## 1. Project Overview

DevMate is a small language model experiment focused on developer assistance. The project uses Qwen3-0.6B as its base model and explores parameter-efficient fine-tuning with LoRA.

The initial goal is to establish a baseline, prepare separate training and evaluation datasets, fine-tune the model locally, and compare its responses against the original model.

## 2. Baseline Configuration

- **Base model:** `Qwen/Qwen3-0.6B`
- **Inference device:** CPU
- **Framework:** PyTorch and Transformers
- **Fine-tuning method:** LoRA using PEFT
- **Initial baseline status:** Recorded before fine-tuning

## 3. Initial Baseline Test

### Prompt

Explain what a Python function is in simple terms. Give one short code example.

### Observed Result

The original model explained that a function is a reusable block of code, described parameters and return values, and provided a valid `add_numbers(a, b)` example.

### Initial Assessment

- Basic explanation: Successful
- Code example: Appropriate
- Readability: Good
- Baseline recorded: Yes

This was one qualitative test and was not intended to be a comprehensive benchmark.

## 4. Dataset Preparation

The project uses separate JSONL files for training and evaluation.

| Dataset | Examples | Purpose |
|---|---:|---|
| `data/train.jsonl` | 8 | Fine-tuning |
| `data/eval.jsonl` | 4 | Evaluation |

The datasets contain developer-focused questions covering Python programming, debugging, Git, and related concepts.

The dataset validation script completed successfully for both files.

## 5. First LoRA Fine-Tuning Experiment

### Configuration

- **Base model:** `Qwen/Qwen3-0.6B`
- **Fine-tuning method:** LoRA using PEFT
- **Training examples:** 8
- **Evaluation examples:** 4
- **Epochs:** 2
- **Learning rate:** `0.0001`
- **Training batch size:** 1
- **Gradient accumulation steps:** 4
- **Maximum sequence length:** 256 tokens
- **Trainable parameters:** 2,293,760
- **Total model parameters:** 598,343,680
- **Trainable parameter percentage:** 0.3834%
- **Training device:** CPU
- **Reported training runtime:** 39.55 seconds
- **Adapter output directory:** `results/devmate-lora/`

### Training Metrics

| Metric | Result |
|---|---:|
| Final training loss | 2.272 |
| Evaluation loss after epoch 1 | 2.340 |
| Evaluation loss after epoch 2 | 2.296 |
| Training runtime | 39.55 seconds |

Evaluation loss decreased by 0.044 between the first and second epochs.

This is an encouraging initial observation, but the evaluation dataset contains only four examples. The decrease does not establish that the model generalizes better to unseen developer questions.

## 6. Qualitative Comparison

The base model and fine-tuned DevMate were tested with the same three prompts.

### Test A: Python Dictionaries

The fine-tuned model produced a more concise definition and a short code example. However, it omitted useful details included in the base model's response and made an imprecise statement about an empty dictionary.

**Assessment:** More concise, but not demonstrably better.

### Test B: Git Fetch Versus Git Pull

Both models described the basic purpose of the two commands. Their captured responses were incomplete, so a reliable comparison of completeness and technical accuracy was not possible.

**Assessment:** Inconclusive.

### Test C: Debugging a Python TypeError

The fine-tuned model provided a short debugging checklist, but it repeated an example error and included potentially misleading advice. The base model's captured response also contained inaccuracies and was incomplete.

**Assessment:** Both responses need improvement.

## 7. Current Findings

- The LoRA training pipeline completed successfully on CPU.
- The trained adapter was saved locally.
- The evaluation script successfully loaded the base model and the fine-tuned adapter.
- The evaluation loss decreased slightly across the two epochs.
- The initial qualitative comparison did not demonstrate a clear improvement in answer quality.

Successful fine-tuning execution should not be confused with proven model improvement.

## 8. Limitations

- The training dataset contains only eight examples.
- The evaluation dataset contains only four examples.
- Training was limited to two epochs.
- The qualitative comparison covered only three prompts.
- Generated answers were limited to 160 new tokens during comparison.
- Some captured answers ended before the explanation was complete.
- No comprehensive benchmark or statistical performance analysis was performed.

## 9. Next Steps

1. Expand the curated developer-focused training dataset.
2. Add more diverse evaluation examples without including them in training.
3. Improve evaluation output length and completeness.
4. Assess correctness, relevance, clarity, and code validity using a consistent rubric.
5. Compare the base and fine-tuned models on identical prompts.
6. Record future experiments and compare their results.
7. Keep generated model artifacts separate from the source code repository.

## 10. Reproducibility and Artifact Management

The training code, dataset files, configuration, and documentation should be version-controlled.

The locally generated adapter and training checkpoints are excluded from the Git repository to avoid committing model artifacts and intermediate training state. They can be regenerated by running the training pipeline with the documented configuration and datasets.

The current adapter is stored locally at `results/devmate-lora/`.

## 11. Conclusion

DevMate's first LoRA experiment successfully demonstrated a local fine-tuning workflow using Qwen3-0.6B, PEFT, and CPU-based training.

The experiment provides a working foundation for further development. However, the available evidence is insufficient to claim that fine-tuning has improved the model's overall programming assistance quality.

The next phase will focus on better datasets, more representative evaluation, and measurable improvements in answer quality.
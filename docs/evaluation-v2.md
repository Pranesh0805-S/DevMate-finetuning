# DevMate V2 — Model Evaluation Report

## 1. Overview

This report documents the second fine-tuning experiment for DevMate, a small language model adapted for programming assistance using LoRA (Low-Rank Adaptation).

The experiment compares three variants:

- **Base model:** `Qwen/Qwen3-0.6B`
- **DevMate V1:** The adapter trained using the initial dataset of 8 examples.
- **DevMate V2:** The adapter trained using an expanded dataset of 50 examples.

The goal was to investigate whether fine-tuning could produce useful programming answers while keeping the model practical to run on CPU-only hardware.

## 2. Experimental Setup

| Setting | Value |
|---|---|
| Base model | `Qwen/Qwen3-0.6B` |
| Fine-tuning method | LoRA |
| Training examples for V1 | 8 |
| Training examples for V2 | 50 |
| Evaluation examples | 21 |
| Training epochs | 2 |
| Maximum sequence length | 256 tokens |
| Device | CPU |
| Evaluation generation | Greedy decoding |

The evaluation script generated answers from the base model, V1, and V2 using the same 21 evaluation questions.

The evaluation dataset was kept separate from the training questions, with no exact question overlaps identified.

## 3. V2 Training Results

The V2 training run completed successfully.

| Metric | Result |
|---|---:|
| Training runtime | 166.4 seconds |
| Training loss | 2.293 |
| Evaluation loss, epoch 1 | 2.172 |
| Evaluation loss, epoch 2 | 2.072 |
| Trainable parameters | 2,293,760 |
| Total parameters | 598,343,680 |
| Trainable parameter percentage | 0.3834% |

The LoRA adapter was saved to `results/devmate-lora-v2`.

The decrease in evaluation loss across V2's two epochs is an encouraging training signal. However, it does not establish that V2 produces more accurate answers than the base model or V1.

V1 and V2 used different evaluation datasets, so their evaluation losses should not be treated as a direct performance comparison.

## 4. Qualitative Evaluation

The 21 evaluation questions covered Python fundamentals, exceptions, collections, Git, HTTP errors, JSON handling, API-key security, unit testing, and Python environments and packages.

### Observed strengths

- V2 often produced shorter, more direct answers.
- V2 correctly explained several basic concepts, including dictionaries, safe integer conversion, and the general meaning of HTTP 404 and HTTP 500.
- The evaluation script successfully generated and saved outputs for all three model variants.

### Observed weaknesses

The following issues appeared in the generated answers:

- **Exception handling:** V2 provided a problematic example that raises `SystemExit` before printing the traceback.
- **Algorithm edge cases:** V2's largest-number example initialized the result to zero, which fails for a list containing only negative numbers.
- **Python exceptions:** V2 incorrectly associated a missing list index with `KeyError`; list indexing normally raises `IndexError`.
- **Git troubleshooting:** Some answers were unclear or potentially risky when discussing commits made on the wrong branch.
- **Security guidance:** V2 did not provide a complete Python example for reading API keys securely.
- **Testing examples:** Some answers described testing without demonstrating a complete, meaningful application test.
- **Answer completeness:** Some responses were concise but omitted useful implementation details or runnable examples.

The base model and V1 also produced incorrect, incomplete, or unnecessarily repetitive answers. Neither should be considered a consistently correct reference.

## 5. Evaluation Limitations

This experiment has several limitations:

1. The review was qualitative; no formal correctness score was calculated.
2. The evaluation set contains only 21 examples and cannot represent all programming tasks.
3. The training dataset is small, so the adapter may overfit to its training examples.
4. A shorter answer is not necessarily more accurate or useful.
5. Training and evaluation loss do not directly measure factual correctness or code execution success.
6. No comprehensive automated code-execution benchmark or statistical significance analysis was performed.

Consequently, this experiment does not establish that V2 outperforms the base model overall.

## 6. Conclusions

DevMate V2 demonstrates that the LoRA training and evaluation pipeline works on the available CPU-only laptop.

The experiment also shows that fine-tuning does not automatically guarantee better programming assistance. The next iteration should prioritize correctness, complete examples, edge-case coverage, and safer troubleshooting guidance.

## 7. Planned Improvements

The next experiment should focus on:

- Reviewing and correcting inaccurate training examples.
- Adding verified examples for exceptions, Git recovery, negative numbers, package management, and API-key handling.
- Evaluating answers against a consistent test set.
- Adding a repeatable scoring rubric for correctness, completeness, relevance, and safety.
- Where practical, running unit tests or code snippets to verify generated code.
- Recording the exact dataset version and training configuration for each experiment.

V3 should be trained only after the dataset and evaluation process have been improved.

## 8. Reproducibility Notes

The evaluation outputs were saved locally in `results/model-comparison.jsonl`. The model adapters and generated results are excluded from Git by the repository's ignore rules.

To reproduce the experiment, use the recorded source code, dataset, model identifier, and training settings. Confirm that the required dependencies and model access are available before running the scripts.

# DevMate V3 — Model Evaluation Report

## 1. Overview

This report documents the third DevMate fine-tuning experiment. It uses LoRA (Low-Rank Adaptation) to adapt `Qwen/Qwen3-0.6B` for programming assistance on CPU-only hardware.

The experiment compares four model variants:

- **Base model:** `Qwen/Qwen3-0.6B`
- **DevMate V1:** Adapter trained using 8 examples.
- **DevMate V2:** Adapter trained using 50 examples.
- **DevMate V3:** Adapter trained using 58 examples, including additional targeted programming and troubleshooting examples.

The objectives were to validate the training pipeline, investigate common answer failures, and establish a repeatable human-evaluation process.

## 2. Experimental Setup

| Setting | Value |
|---|---|
| Base model | `Qwen/Qwen3-0.6B` |
| Fine-tuning method | LoRA |
| V1 training examples | 8 |
| V2 training examples | 50 |
| V3 training examples | 58 |
| Evaluation questions | 21 |
| Training epochs | 2 |
| Maximum sequence length | 256 tokens |
| Learning rate | 0.0001 |
| Device | CPU |
| Evaluation generation | Greedy decoding |

V3 training completed in approximately 194.9 seconds over 30 optimizer steps. The adapter was saved locally to `results/devmate-lora-v3`.

The evaluation script generated responses from the base model and all three adapters for the same 21 questions. The questions cover Python fundamentals, exceptions, collections, Git, HTTP errors, JSON handling, API-key security, unit testing, and Python environments.

**Dataset limitation:** No exact question-text overlaps were identified between the training and evaluation files. However, some V3 training examples were deliberately added to address weaknesses observed in the existing evaluation topics. Consequently, this evaluation set should be treated as a development set, not an independent final test set.

## 3. V3 Training Results

| Metric | Result |
|---|---:|
| Training runtime | 194.9 seconds |
| Training steps | 30 |
| Training loss | 2.284 |
| Evaluation loss, epoch 1 | 2.115 |
| Evaluation loss, epoch 2 | 2.030 |
| Trainable parameters | 2,293,760 |
| Total parameters | 598,343,680 |
| Trainable parameter percentage | 0.3834% |

The evaluation loss decreased across V3's two training epochs. This is a useful training signal, but it does not establish that the model's generated answers became more accurate or useful.

Loss values from V1, V2, and V3 should not be used as a direct performance ranking because the experiments used different training datasets and configurations over time.

## 4. Human Evaluation Results

Each model's 21 responses was reviewed using three ratings on a scale from 1 to 5:

- **Correctness:** Technical accuracy.
- **Relevance:** How directly the response addresses the question.
- **Usefulness:** How actionable and helpful the response is.

Reviewers also recorded whether each response contained a critical error. The three rating categories were aggregated into a combined score out of a maximum of 315 points per model.

| Model | Correctness points | Relevance points | Usefulness points | Critical errors | Combined score |
|---|---:|---:|---:|---:|---:|
| Base model | 67/105 | 100/105 | 67/105 | 11 | 74.29% |
| DevMate V1 | 76/105 | 99/105 | 74/105 | 7 | 79.05% |
| DevMate V2 | 79/105 | 90/105 | 58/105 | 4 | 72.06% |
| DevMate V3 | 80/105 | 90/105 | 61/105 | 2 | 73.33% |

### Interpretation

- **V1 achieved the highest combined score**, at 79.05%.
- **V3 achieved the highest correctness subtotal**, at 80/105.
- **V3 had the fewest flagged critical errors**, with 2 across the 21 reviewed responses.
- V3's combined score was 73.33%, below the base model's 74.29% and V1's 79.05%.
- V3's usefulness subtotal was 61/105, indicating room to improve answer completeness and practical guidance.

These findings show mixed results. V3 performed best on the correctness subtotal and had the fewest flagged critical errors, but it did not achieve the highest combined score.

The scores reflect the current manually reviewed development set. They do not establish that V3 is generally superior to the other models or that the observed differences will hold on unseen tasks.

## 5. Observed Strengths and Weaknesses

### Strengths

- The V3 fine-tuning run completed successfully on CPU-only hardware.
- The evaluation script generated responses for all four model variants.
- The review process recorded correctness, relevance, usefulness, and critical-error judgments.
- V3 received the highest correctness subtotal and the lowest critical-error count in this evaluation.

### Remaining Weaknesses

The reviewed responses identified several areas that need further improvement:

- **Exception handling:** Some responses used incorrect traceback-handling sequences or lacked complete runnable examples.
- **Algorithm edge cases:** The largest-number task exposed a failure when an implementation initializes its result to zero and receives only negative values.
- **Python exceptions:** Some responses confused `KeyError` with `IndexError`.
- **Git recovery:** Wrong-branch recovery guidance was sometimes vague or potentially destructive.
- **Pushed commits:** Some responses did not clearly distinguish the safe use of `git revert` from rewriting shared history.
- **Package management:** Some responses omitted the complete command `python -m pip freeze > requirements.txt`.
- **API-key security:** Some responses lacked a concrete, secure Python example.
- **Testing and debugging:** Several responses needed clearer examples and more actionable steps.

The base model and earlier adapters also produced incorrect or incomplete responses. No model should be considered consistently reliable based on this experiment alone.

## 6. Evaluation Limitations

1. **Small sample size:** The evaluation contains only 21 questions and covers a limited range of programming tasks.
2. **Development-set exposure:** The existing evaluation topics were used to identify weaknesses and inform some V3 training examples.
3. **Subjective ratings:** Human judgments can vary between reviewers.
4. **Custom scoring rubric:** The combined score is a rubric-based summary, not a standardized benchmark.
5. **Critical-error judgments:** Critical-error counts depend on the reviewer's interpretation of severity.
6. **Limited execution testing:** No comprehensive automated code-execution benchmark was run.
7. **Loss limitations:** Training and evaluation loss do not directly measure factual correctness, successful code execution, or real-world usefulness.
8. **No generalization evidence:** The results do not establish statistical significance or reliable performance on unseen programming tasks.

The results should therefore be treated as preliminary development findings, not independent evidence of broad model improvement.

## 7. Conclusions

DevMate V3 demonstrates that the expanded LoRA training pipeline can run successfully on the available CPU-only laptop.

On the current 21-question development evaluation, V3 received the highest correctness subtotal and the fewest flagged critical errors. However, V1 retained the highest combined score, and V3's combined score was slightly below that of the base model.

These mixed results demonstrate why training loss alone is insufficient to evaluate a programming assistant. They also highlight the need to assess technical accuracy, practical usefulness, and critical failures separately.

The next priority is to create a fresh test set that has not influenced training decisions, validate generated code where practical, and review the scoring records for consistency before making stronger claims about model quality.

## 8. Planned Improvements

- Build a new test set containing questions that were not used to guide V3 dataset changes.
- Include algorithmic edge cases, multi-step debugging, and realistic programming tasks.
- Run automated tests against generated code where safe and practical.
- Improve training examples for Python exceptions, Git recovery, package management, and API-key handling.
- Review critical-error decisions and rating consistency.
- Record dataset versions, training settings, evaluation procedures, and model revisions.
- Compare future experiments against the same held-out test set.
- Track correctness, usefulness, and critical errors separately rather than relying only on the combined score.

## 9. Reproducibility Notes

The V3 adapter, model-comparison output, correctness-review records, and generated scorecard are stored locally under `results/` and excluded from Git by the repository's ignore rules.

The scorecard is generated by `src/final_scorecard.py` from the human-review records. Its validation checks the expected question count and required rating fields; it does not independently verify whether individual ratings are correct.

The training and evaluation scripts, datasets, and documentation should be versioned so that the experiment's setup can be inspected. Model weights and raw generated outputs do not need to be committed to the repository.

Because the evaluation set influenced development decisions, future performance claims should be based on a separately maintained test set that remains untouched during training and iteration.

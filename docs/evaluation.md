# DevMate Evaluation Guide

## Overview

DevMate evaluation compares the base `Qwen/Qwen3-0.6B` model with fine-tuned DevMate adapters.

The project evaluates generated answers using technical correctness, relevance, practical usefulness, and a critical-error flag.

The current V3 report describes a 21-question human-rated development evaluation. It is preliminary and is not an independent benchmark.

## Evaluation Workflow

The evaluation workflow has three main stages:

1. Generate answers from the base model and available DevMate adapters.
2. Review the generated answers using the project's rating criteria.
3. Aggregate the review records into a scorecard.

The generation scripts and scorecard utilities have different input requirements. Review the relevant script before running a stage.

## Prerequisites

- Install dependencies as described in the [Training Guide](training.md).
- Ensure `data/eval.jsonl` exists and contains valid evaluation examples.
- Ensure the local adapter directories required by the comparison script exist.
- Ensure the expected review records are available before generating the final scorecard.

The trained adapters and local review records are not included in a fresh Git checkout.

## 1. Generate Model Comparisons

Run:

```powershell
python src/evaluate_model.py
```

The current script loads the base model and these adapters:

- `results/devmate-lora`
- `results/devmate-lora-v2`
- `results/devmate-lora-v3`

It reads questions from `data/eval.jsonl` and writes the generated comparison records to:

```text
results/model-comparison-v3.jsonl
```

This step generates model responses; it does not assign human ratings or establish that one model is better than another.

## 2. Review Generated Answers

Evaluate the answers using consistent criteria:

- **Technical correctness:** Is the answer factually and technically accurate?
- **Relevance:** Does it directly address the question?
- **Practical usefulness:** Does it provide actionable, appropriately detailed help?
- **Critical error:** Does it contain a serious mistake that could materially mislead the user or cause harm?

The current V3 review used a 1–5 scale for each of the three rating categories and separately recorded critical errors.

Apply the same rubric consistently across model variants. When possible, review answers without knowing which model generated them to reduce bias.

## 3. Generate the Scorecard

The current scorecard utility expects manually reviewed records at:

```text
results/correctness-review.fresh.jsonl
```

When those records are available, run:

```powershell
python src/final_scorecard.py
```

The script validates the required model ratings and expected question IDs, aggregates the scores, and writes:

```text
results/final-scorecard.json
```

The scorecard script validates the structure and range of the supplied ratings. It does not independently verify whether the ratings themselves are correct.

**Important:** The review-record input is local and is not included in the repository. A fresh clone cannot generate the final scorecard unless the required review records are supplied or recreated.

## Scoring Methodology

Each answer receives three ratings, each from 1 to 5:

- Technical correctness
- Relevance
- Practical usefulness

For 21 reviewed answers, each category has a maximum of 105 points. The combined score is calculated as:

`Combined score (%) = earned points / maximum points * 100`

With three categories and 21 answers, the maximum combined score is 315 points.

Critical errors are counted separately. They are not subtracted from the combined score by the current scorecard script.

A higher combined score does not automatically mean a model is safer or more reliable. Review the category subtotals and critical-error count alongside the overall percentage.

## V3 Evaluation Results

The documented V3 development evaluation reported:

| Model | Correctness | Relevance | Usefulness | Critical errors | Combined score |
|---|---:|---:|---:|---:|---:|
| Base model | 67/105 | 100/105 | 67/105 | 11 | 74.29% |
| DevMate V1 | 76/105 | 99/105 | 74/105 | 7 | 79.05% |
| DevMate V2 | 79/105 | 90/105 | 58/105 | 4 | 72.06% |
| DevMate V3 | 80/105 | 90/105 | 61/105 | 2 | 73.33% |

V3 achieved the highest correctness subtotal and had the fewest flagged critical errors in this review. V1 achieved the highest combined score.

Some V3 training examples were informed by weaknesses observed in the evaluation topics. These results therefore represent a development evaluation, not an independent measurement of generalization.

See the [DevMate V3 Model Evaluation Report](evaluation-v3.md) for the detailed findings, weaknesses, and limitations.

## Evaluation Limitations

- The current evaluation set contains only 21 questions.
- Some evaluation topics informed V3 training-data changes.
- Human ratings can be subjective.
- Critical-error classifications depend on reviewer judgment.
- The current workflow does not run a comprehensive automated code-execution benchmark.
- The scorecard is a custom rubric, not a standardized external benchmark.
- Training loss and evaluation loss do not directly establish answer quality.

## Recommendations for Future Versions

- Maintain a held-out test set that does not influence training decisions.
- Expand coverage to realistic programming, debugging, and edge-case tasks.
- Run generated code in a controlled test environment where appropriate.
- Keep scoring criteria consistent across model versions.
- Record dataset versions, configurations, and evaluation results for each experiment.
- Track correctness, usefulness, and critical errors separately.

## Related Documentation

- [Project README](../README.md)
- [Training Guide](training.md)
- [V3 Evaluation Report](evaluation-v3.md)
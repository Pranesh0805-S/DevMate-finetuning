# DevMate Training Guide

## Overview

DevMate is an experimental small language model project that fine-tunes `Qwen/Qwen3-0.6B` using Low-Rank Adaptation (LoRA).

The V3 experiment was trained on CPU using Python, PyTorch, Hugging Face Transformers, and PEFT. Training results are preliminary and do not by themselves establish improved model quality.

## Prerequisites

- Windows 11 or a compatible Python environment
- Python 3.12.10 for the documented V3 setup
- Git
- Sufficient RAM and disk space for the base model, dependencies, and training outputs
- Internet access for downloading the base model and tokenizer on the first run

CPU training is supported by the project's V3 configuration but can be slow. Runtime and memory requirements vary by environment.

## 1. Clone the repository

```powershell
git clone https://github.com/Pranesh0805-S/DevMate-finetuning.git
cd DevMate-finetuning
```

## 2. Create and activate a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, use an appropriate local execution-policy setting or invoke the virtual environment's Python executable directly.

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The repository pins dependency versions, including a CPU-only PyTorch build. Installation compatibility depends on the operating system, Python version, and available packages.

## 4. Prepare the datasets

The training script expects these files:

- `data/train.jsonl`
- `data/eval.jsonl`

Each non-empty JSONL record must contain a `messages` array representing a conversation. The final message must be an assistant response. Dataset records should contain valid, non-empty message content.

Validate the datasets before training:

```powershell
python src/prepare_dataset.py
```

The script validates both expected dataset paths. Keep evaluation examples separate from training examples and avoid using held-out test results to guide training changes.

## 5. Train the model

Run:

```powershell
python src/train.py
```

The current training script uses:

| Setting | Value |
|---|---|
| Base model | `Qwen/Qwen3-0.6B` |
| Fine-tuning method | LoRA |
| Training device | CPU |
| Epochs | 2 |
| Maximum sequence length | 256 tokens |
| Per-device training batch size | 1 |
| Gradient accumulation steps | 4 |
| Learning rate | `0.0001` |
| LoRA rank | 8 |
| LoRA alpha | 16 |
| LoRA dropout | 0.05 |

These values describe the current script, not a guarantee that every future DevMate version will use the same configuration.

## 6. Training outputs

The script saves the adapter and tokenizer to:

```text
results/devmate-lora-v3/
```

Training checkpoints and generated results are local artifacts and are excluded from Git by the repository's ignore rules.

Do not assume a fresh clone contains the trained adapter. The base model and tokenizer may need to be downloaded, and the local dataset files must be present.

## 7. Run the tests

```powershell
python -m pytest tests -q
```

The current automated tests validate dataset preparation behavior. Passing them does not establish that the fine-tuned model produces correct answers.

## Troubleshooting

### Dataset file not found

Confirm that `data/train.jsonl` and `data/eval.jsonl` exist in the repository root and contain valid JSONL records.

### Invalid JSON or conversation structure

Run the dataset validator and inspect the reported line number. Each record must contain a valid `messages` array with non-empty message content and the expected conversation roles.

### Missing dependency

Ensure the virtual environment is active and install dependencies using:

```powershell
python -m pip install -r requirements.txt
```

### Insufficient memory or slow training

CPU training may take several minutes or longer depending on the dataset and hardware. Close unnecessary applications and check available memory before retrying. Do not change training settings without recording the change.

### Adapter not found during evaluation

Verify that the expected adapter directory exists under `results/`. Evaluation scripts that compare model variants require the corresponding local adapters to be available.

## Related documentation

- [Project README](../README.md)
- [V3 Evaluation Report](evaluation-v3.md)
- [Evaluation Instructions](evaluation.md)

## Reproducibility notes

Record the dataset version, configuration, dependency versions, training duration, and resulting evaluation metrics for each experiment. Treat V3's existing human-rated evaluation as a development evaluation rather than an independent benchmark.
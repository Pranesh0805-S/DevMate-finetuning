# DevMate — Small LLM Fine-Tuning

**An experimental developer-focused language model built by fine-tuning Qwen3-0.6B with Low-Rank Adaptation (LoRA).**

DevMate investigates how targeted training examples can influence a small language model’s responses to practical programming questions and developer workflows. The project combines parameter-efficient fine-tuning, structured evaluation, and automated testing to analyze model behavior and response quality.

> **Status:** Experimental research project. Evaluation results are preliminary and do not establish general improvements across tasks or domains.

## Project Goals

- Fine-tune a compact language model using LoRA.
- Build a reproducible dataset preparation and training pipeline.
- Compare the base model against successive DevMate versions.
- Evaluate generated answers for technical correctness, relevance, practical usefulness, and critical errors.
- Document limitations and use evaluation findings to guide future experiments.

## Technology Stack

- **Base model:** `Qwen/Qwen3-0.6B`
- **Fine-tuning:** Hugging Face Transformers and PEFT (LoRA)
- **Dataset tooling:** Hugging Face Datasets
- **Training framework:** PyTorch
- **Language:** Python
- **Testing:** pytest

## Development Environment

The V3 experiment was run on:

| Component | Configuration |
|---|---|
| Processor | AMD Ryzen 7 7730U |
| Memory | 16 GB RAM |
| Operating system | Windows 11 |
| Python | 3.12.10 |
| Training device | CPU |
| Fine-tuning method | LoRA |

## DevMate V3 Experiment

The V3 training run used:

- 58 training examples
- 2 training epochs
- 30 optimizer steps
- Approximately 194.9 seconds of CPU training
- 2,293,760 trainable parameters out of 598,343,680 total parameters (approximately 0.3834%)

The reported training loss was 2.284. Evaluation loss reached 2.030 during the run. Loss values alone do not establish that answers are more accurate or useful.

The trained adapter is stored locally under `results/devmate-lora-v3`. Model weights and generated results are excluded from version control where configured by `.gitignore`.

## Evaluation Results

The V3 evaluation compared four variants across 21 programming and developer-workflow questions. Each answer was reviewed using a 1–5 rating scale for technical correctness, relevance, and practical usefulness, alongside a critical-error flag.

| Model | Correctness | Relevance | Usefulness | Critical errors | Combined score |
|---|---:|---:|---:|---:|---:|
| Base model | 67/105 | 100/105 | 67/105 | 11 | 74.29% |
| DevMate V1 | 76/105 | 99/105 | 74/105 | 7 | 79.05% |
| DevMate V2 | 79/105 | 90/105 | 58/105 | 4 | 72.06% |
| DevMate V3 | 80/105 | 90/105 | 61/105 | 2 | 73.33% |

### Interpreting the results

- V3 achieved the highest technical-correctness subtotal in this review.
- V3 had the fewest flagged critical errors.
- V1 achieved the highest combined score.
- V3's combined score was below both the base model and V1.

These results do **not** demonstrate an overall improvement from fine-tuning. The evaluation contains only 21 questions, relies on human ratings, and has semantic overlap between some evaluation topics and training examples. It is a development evaluation, not an independent benchmark. The ratings and audit notes have not been independently validated.

See [`docs/evaluation-v3.md`](docs/evaluation-v3.md) for the detailed report.

## Repository Structure

```text
DevMate-finetuning/
├── configs/       # Training configuration
├── data/          # Dataset files
├── docs/          # Evaluation reports and documentation
├── examples/      # Example resources
├── src/           # Dataset preparation, training and evaluation scripts
├── tests/         # Automated tests
├── results/       # Local training outputs, adapters and evaluation artifacts
├── .gitignore
└── requirements.txt
```

Generated outputs and local review records may not be included in a Git checkout. Check the relevant scripts and configuration before running a workflow that depends on them.

## Setup on Windows

### 1. Clone the repository

```powershell
git clone https://github.com/Pranesh0805-S/DevMate-finetuning.git
cd DevMate-finetuning
```

### 2. Create a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, use an approved local execution-policy setting or invoke the environment's Python executable directly.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The pinned dependencies include CPU-only PyTorch. Training speed and compatibility depend on the Python version, installed packages, available memory, and hardware.

### 4. Run the tests

```powershell
python -m pytest tests -q
```

The test suite covers dataset preparation and review CLI behavior. Passing these tests does not verify model answer quality or independently validate the evaluation ratings.

## Training and Evaluation

The repository contains scripts for dataset preparation, fine-tuning, model evaluation, and scorecard generation.

Inspect the relevant script's configuration and input/output paths before running it. Some workflows require locally generated files or review data that are not tracked in Git.

Typical commands used by this project include:

```powershell
python -m pytest tests -q
python src/evaluate_model.py
python src/final_scorecard.py
```

The evaluation and scorecard commands require their expected input files to exist under `results/`. Follow the instructions in the evaluation documentation and scripts before running them.

## Limitations

- The model is small and may produce incorrect, incomplete, or misleading programming advice.
- CPU fine-tuning is relatively slow.
- The evaluation set is small and not independent of the training topics.
- Human-assigned ratings can be subjective.
- Automated tests validate selected pipeline behavior, not general model intelligence.
- Adapter weights and evaluation artifacts may need to be generated locally.

Do not use DevMate's output as a substitute for testing code, checking official documentation, or reviewing security-sensitive changes.

## Roadmap

- Improve dataset coverage and quality.
- Reduce overlap between training examples and evaluation questions.
- Build a separate held-out test set.
- Add repeatable evaluation procedures and stronger validation.
- Investigate V4 improvements using documented failure cases.

## License

No license is declared here. Unless a license is added to the repository, reuse and redistribution permissions should not be assumed. The base model and its dependencies may have separate license terms.

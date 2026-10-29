# DevMate — Small LLM Fine-Tuning

An experimental developer-focused language model built by fine-tuning Qwen3-0.6B with Low-Rank Adaptation (LoRA).

DevMate explores how targeted training examples influence a small language model's responses to programming questions and developer workflows. The project combines parameter-efficient fine-tuning, structured evaluation, an installable Python client, automated testing, and continuous integration.

> **Project status:** Experimental research project. Evaluation results are preliminary and do not establish general improvements across tasks or domains.

## Project Goals

- Fine-tune a compact language model using LoRA.
- Build a reproducible dataset preparation and training pipeline.
- Compare the base model against successive DevMate versions.
- Evaluate technical correctness, relevance, usefulness, and critical errors.
- Provide a Python client for loading the adapter and generating responses.
- Automate testing and code-quality checks through GitHub Actions.
- Document limitations and use evaluation findings to guide future experiments.

## Technology Stack

| Component | Technology |
|---|---|
| Base model | Qwen/Qwen3-0.6B |
| Fine-tuning | Hugging Face Transformers and PEFT (LoRA) |
| Dataset tooling | Hugging Face Datasets |
| Training framework | PyTorch |
| Programming language | Python |
| Package build | setuptools and `pyproject.toml` |
| Automated testing | pytest |
| Linting | Ruff |
| Continuous integration | GitHub Actions |
| Model hosting | Hugging Face |

## Development Environment

The DevMate V3 training experiment was conducted on the following hardware:

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
- 2,293,760 trainable parameters out of 598,343,680 total parameters
- Approximately 0.3834% trainable parameters

The reported training loss was 2.284, and evaluation loss reached 2.030 during the run. Loss values alone do not establish that generated answers are more accurate or useful.

### Model access

The trained adapter is hosted in the [DevMate V3 Hugging Face repository](https://huggingface.co/Pranesh0805-S/DevMate-V3).

**The adapter repository is currently private.** Users must have permission to access it and authenticate with Hugging Face. The package does not bundle the base model or adapter weights.

## Python Client

The repository includes an installable Python package named `pranesh-devmate-toolkit`, version `0.1.0`. Its Python import name is `devmate`.

The client loads the Qwen3-0.6B base model and the DevMate V3 LoRA adapter, then provides a `generate()` method for text generation.

### Installation from a local checkout

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/Pranesh0805-S/DevMate-finetuning.git
cd DevMate-finetuning

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The editable installation installs the client and its development dependencies, including pytest and Ruff.

### Usage

```python
from devmate import DevMate

model = DevMate()

answer = model.generate(
    "Explain Python functions with an example."
)

print(answer)
```

The first initialization downloads required model files if they are not already cached. Access to the private Hugging Face adapter is required.

The client defaults to:

- Base model: `Qwen/Qwen3-0.6B`
- Adapter: `Pranesh0805-S/DevMate-V3`
- Maximum generated tokens: 180
- Device: CUDA when available, otherwise CPU
- Base model precision: float32

Loading the model can consume substantial memory, and CPU generation may be slow.

### Build the package

Install the build tool and create the distribution files:

```powershell
python -m pip install build
python -m build
```

The command produces a wheel and source distribution in `dist/`.

The wheel contains the Python client, not the Qwen base model or DevMate adapter weights.

### Clean-Environment Verification

The package was tested in a separate virtual environment, independent of the original development environment.

Verified results:

- Built the Python wheel successfully.
- Created a fresh virtual environment.
- Installed the model runtime dependencies.
- Installed the built wheel.
- Verified that `from devmate import DevMate` succeeds.
- Loaded the model adapter and generated a Python example.
- Confirmed that automated tests and Ruff checks pass.

The inference check successfully generated a Python function example. This verifies a working inference path for the tested environment, not compatibility with every dependency version or general model answer quality.

## Testing and Code Quality

### Run automated tests

Run the test suite from the repository root:

```powershell
python -m pytest -q tests/
```

**Latest recorded local result: 22 tests passed.**

The tests cover selected dataset, review CLI, and Python client validation behavior. Passing tests does not independently validate the model's general intelligence or evaluation ratings.

### Run Ruff

Check the source code and tests for linting issues:

```powershell
python -m ruff check src tests
```

The configured Ruff checks passed locally.

The `TRY004` rule is intentionally ignored in `pyproject.toml` to preserve the current validation exception behavior.

### Continuous integration

GitHub Actions runs the automated checks on pushes and pull requests.

The workflow installs the project dependencies, runs Ruff, and executes the test suite.

The latest recorded workflow completed successfully with both linting and automated tests passing.

See the [GitHub Actions workflow history](https://github.com/Pranesh0805-S/DevMate-finetuning/actions) for run results.

## Evaluation Results

The V3 evaluation compared four variants across 21 programming and developer-workflow questions. Answers were reviewed on a 1–5 scale for technical correctness, relevance, and practical usefulness, alongside a critical-error flag.

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

These results **do not demonstrate an overall improvement from fine-tuning**. The evaluation contains only 21 questions, relies on human ratings, and has semantic overlap between some evaluation topics and training examples. It is a development evaluation, not an independent benchmark. The ratings and audit notes have not been independently validated.

See [`docs/evaluation-v3.md`](docs/evaluation-v3.md) for the detailed report.

## Repository Structure

```text
DevMate-finetuning/
├── configs/                 # Training configuration
├── data/                    # Dataset files
├── docs/                    # Evaluation reports and documentation
├── examples/                # Client usage examples
├── src/
│   ├── devmate/             # Python client package
│   └── ...                  # Training and evaluation scripts
├── tests/                   # Automated tests
├── results/                 # Local outputs and evaluation artifacts
├── .github/
│   └── workflows/           # GitHub Actions CI
├── pyproject.toml           # Package and Ruff configuration
├── requirements.txt         # Pinned experiment environment
└── .gitignore
```

Generated outputs, model weights, and local review records may be excluded from Git. Check the relevant scripts and configuration before running workflows that depend on local artifacts.

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

### 3. Install project dependencies

The repository provides a pinned `requirements.txt` for the experiment environment and a `pyproject.toml` for the installable Python client.

To install the pinned experiment environment and the client development tools:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e ".[dev]"
```

The requirements file includes CPU-only PyTorch. Training speed and compatibility depend on Python, installed packages, available memory, and hardware.

The editable installation makes the `devmate` package importable from the local checkout.

### 4. Run the tests

```powershell
python -m pytest -q tests/
```

### 5. Check code quality

```powershell
python -m ruff check src tests
```

The client usage example loads the model, so run it separately when you want to perform inference and have access to the private adapter repository.

## Training and Evaluation

The repository contains scripts for dataset preparation, fine-tuning, model evaluation, and scorecard generation.

Inspect the relevant script's configuration and input/output paths before running it. Some workflows require locally generated files or review data that are not tracked in Git.

Typical project commands include:

```powershell
python -m pytest -q tests/
python src/evaluate_model.py
python src/final_scorecard.py
```

The evaluation and scorecard commands require their expected input files to exist under `results/`. Follow the evaluation documentation and script configuration before running them.

## Limitations

- DevMate is a small experimental model and may generate incorrect or misleading programming advice.
- CPU fine-tuning is relatively slow.
- The evaluation set is small and not independent of the training topics.
- Human-assigned ratings can be subjective.
- Automated tests validate selected software behavior, not general model intelligence.
- Model weights and evaluation artifacts may need to be generated locally.
- The Python client currently depends on access to the private Hugging Face adapter repository.
- Successful testing in one clean environment does not guarantee compatibility with every dependency version.

Do not use DevMate's output as a substitute for testing code, checking official documentation, or reviewing security-sensitive changes.

## Roadmap

- Improve dataset coverage and quality.
- Reduce overlap between training examples and evaluation questions.
- Build a separate held-out test set.
- Add repeatable evaluation procedures and stronger validation.
- Investigate V4 improvements using documented failure cases.
- Expand client-specific automated tests.
- Review dependency compatibility and licensing before a public package release.

## License and Distribution

No license is currently declared for this repository. Unless a license is added, reuse and redistribution permissions should not be assumed.

The base model, dependencies, and training dataset may have separate license or usage terms. Before making the adapter public or publishing the package, verify:

- The base model's license and adapter distribution requirements.
- Dataset permissions and redistribution restrictions.
- The intended license for DevMate-specific code and artifacts.
- Dependency licensing and package metadata.

Until those checks are complete, the Hugging Face adapter should remain private.
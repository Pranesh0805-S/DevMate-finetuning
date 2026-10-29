# DevMate — Small LLM Fine-Tuning

**DevMate** is an experimental developer-focused language model project built by fine-tuning [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) using **Low-Rank Adaptation (LoRA)**.

The project explores how targeted training examples affect a compact language model's responses to programming questions and developer workflows. It combines parameter-efficient fine-tuning, dataset preparation, model evaluation, a Python client, a FastAPI service, Docker packaging, automated testing, and continuous integration.

> **Project status:** Experimental research project. Evaluation results are preliminary and do not establish general improvements across tasks or domains.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture and Distribution](#architecture-and-distribution)
- [Technology Stack](#technology-stack)
- [DevMate V3 Training Experiment](#devmate-v3-training-experiment)
- [Model Access on Hugging Face](#model-access-on-hugging-face)
- [Python Client](#python-client)
- [Docker API](#docker-api)
- [Development Setup](#development-setup)
- [Testing and Code Quality](#testing-and-code-quality)
- [Evaluation Results](#evaluation-results)
- [Repository Structure](#repository-structure)
- [Limitations and Security](#limitations-and-security)
- [Roadmap](#roadmap)
- [License and Distribution](#license-and-distribution)

## Project Overview

DevMate aims to investigate how fine-tuning a small language model can influence developer-oriented responses.

Project goals include:

- Fine-tune a compact model using LoRA.
- Maintain a reproducible dataset preparation and training pipeline.
- Compare the base model against successive DevMate versions.
- Evaluate technical correctness, relevance, usefulness, and critical errors.
- Provide a reusable Python client for text generation.
- Expose an experimental HTTP API through FastAPI.
- Distribute the Python toolkit through PyPI and the container image through GitHub Container Registry.
- Automate tests and code-quality checks through GitHub Actions.
- Document limitations and use evaluation findings to guide future experiments.

## Architecture and Distribution

DevMate uses the Qwen3-0.6B base model with a separately hosted LoRA adapter. The Python package provides the client code that loads these components and generates responses.

| Component | Purpose | Location |
|---|---|---|
| Base model | Original pretrained language model | [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) |
| DevMate V3 adapter | Fine-tuned LoRA weights and associated model files | [Hugging Face repository](https://huggingface.co/Pranesh0805-S/DevMate-V3) |
| Python toolkit | Installable client library | [PyPI package](https://pypi.org/project/pranesh-devmate-toolkit/) |
| Docker image | Containerized FastAPI service | `ghcr.io/pranesh0805-s/devmate:0.1.1` |
| Source code | Training, evaluation, client, and project documentation | [GitHub repository](https://github.com/Pranesh0805-S/DevMate-finetuning) |

The Docker image contains the application code and runtime dependencies. It does not bundle the base model or private adapter weights; model files are downloaded when the model is initialized.

## Technology Stack

| Component | Technology |
|---|---|
| Base model | Qwen/Qwen3-0.6B |
| Fine-tuning | Hugging Face Transformers and PEFT (LoRA) |
| Dataset tooling | Hugging Face Datasets |
| Training framework | PyTorch |
| Programming language | Python |
| Python packaging | setuptools and `pyproject.toml` |
| API | FastAPI and Uvicorn |
| Containerization | Docker |
| Container registry | GitHub Container Registry (GHCR) |
| Model hosting | Hugging Face |
| Automated tests | pytest |
| Linting | Ruff |
| Continuous integration | GitHub Actions |

## Development Environment

The DevMate V3 training experiment was conducted using the following environment.

| Component | Configuration |
|---|---|
| Processor | AMD Ryzen 7 7730U |
| Memory | 16 GB RAM |
| Operating system | Windows 11 |
| Python | 3.12.10 |
| Training device | CPU |
| Fine-tuning method | LoRA |

Results and performance may differ on other hardware and software environments.

## DevMate V3 Training Experiment

The recorded V3 training run used:

- **58 training examples**
- **2 training epochs**
- **30 optimizer steps**
- Approximately **194.9 seconds** of CPU training
- **2,293,760 trainable parameters** out of 598,343,680 total parameters
- Approximately **0.3834%** of parameters trainable

The reported training loss was 2.284, and the evaluation loss reached 2.030 during the run. Loss values alone do not establish that generated answers are more accurate or useful.

## Model Access on Hugging Face

The DevMate V3 adapter is hosted at:

**[Pranesh0805-S/DevMate-V3](https://huggingface.co/Pranesh0805-S/DevMate-V3)**

The adapter repository is currently private. Access requires authorization from the repository owner and a Hugging Face token with permission to read the repository.

DevMate uses two model components:

1. **Base model:** `Qwen/Qwen3-0.6B`
2. **Fine-tuned adapter:** `Pranesh0805-S/DevMate-V3`

The adapter contains the LoRA parameters learned during fine-tuning; it is not a standalone full copy of the base model. The client loads the base model and applies the adapter.

Installing the Python package or downloading the Docker image does not grant access to the private adapter. Users must have their own authorized Hugging Face access.

The adapter will remain private until its distribution terms, training-data permissions, and intended licensing have been reviewed.

## Python Client

The published Python distribution is **`pranesh-devmate-toolkit`**, version **`0.1.1`**. Its Python import name is `devmate`.

### Install from PyPI

```bash
python -m pip install pranesh-devmate-toolkit
```

- [PyPI project page](https://pypi.org/project/pranesh-devmate-toolkit/)
- [Version 0.1.1](https://pypi.org/project/pranesh-devmate-toolkit/0.1.1/)

### Usage

```python
from devmate import DevMate

model = DevMate()

answer = model.generate(
    "Explain Python functions with an example."
)

print(answer)
```

The client loads the base model and DevMate V3 adapter, then provides a `generate()` method for text generation.

The first initialization downloads model files if they are not already cached. A Hugging Face token with access to the private adapter must be available in the environment.

The client defaults to:

| Setting | Default |
|---|---|
| Base model | `Qwen/Qwen3-0.6B` |
| Adapter | `Pranesh0805-S/DevMate-V3` |
| Maximum generated tokens | 180 |
| Device | CUDA when available; otherwise CPU |
| Base model precision | float32 |

Model loading can consume substantial memory, and CPU generation may be slow.

## Docker API

DevMate is distributed as a Docker image through GitHub Container Registry.

**Published image:**

```text
ghcr.io/pranesh0805-s/devmate:0.1.1
```

- [View the GitHub repository](https://github.com/Pranesh0805-S/DevMate-finetuning)
- [View GitHub Packages](https://github.com/users/Pranesh0805-S/packages)

The image was built, pushed to GHCR, pulled from the registry, and tested with a successful text-generation request.

### Prerequisites

- Docker Desktop or another working Docker installation.
- A Hugging Face token with permission to access `Pranesh0805-S/DevMate-V3`.
- Sufficient available memory and disk space to download and load the model.

### 1. Enter your Hugging Face token

In PowerShell, enter your token without displaying it:

```powershell
$secureToken = Read-Host "Enter your Hugging Face token" -AsSecureString
$env:HF_TOKEN = [System.Net.NetworkCredential]::new("", $secureToken).Password
```

Do not commit the token, include it in the Docker image, or share it publicly.

### 2. Pull the image

```powershell
docker pull ghcr.io/pranesh0805-s/devmate:0.1.1
```

### 3. Start the API

```powershell
docker run -d `
  --name devmate-api `
  -p 8000:8000 `
  -e HF_TOKEN `
  -v devmate-cache:/models/cache `
  ghcr.io/pranesh0805-s/devmate:0.1.1
```

The named volume preserves the Hugging Face cache between container recreations.

### 4. Check the health endpoint

Open:

[http://localhost:8000/health](http://localhost:8000/health)

Expected response:

```json
{
  "status": "ok",
  "service": "devmate-api"
}
```

### 5. Open the interactive API documentation

Visit:

[http://localhost:8000/docs](http://localhost:8000/docs)

The API exposes these endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Check whether the API service is responding |
| `/generate` | POST | Generate a response from a text prompt |

### 6. Generate a response

In PowerShell:

```powershell
$body = @{
    prompt = "Explain what a Python function is with a simple example."
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://localhost:8000/generate `
  -Method Post `
  -ContentType "application/json" `
  -Body $body `
  -TimeoutSec 300
```

The first generation may take longer while the model files are downloaded and initialized.

To view application logs:

```powershell
docker logs devmate-api
```

To stop and remove the container:

```powershell
docker stop devmate-api
docker rm devmate-api
```

The cache volume can be retained for future runs.

> **Security warning:** The current API does not implement its own authentication or rate limiting. Keep it accessible only on your local machine unless you add appropriate access controls before deployment.

## Development Setup

To work on the repository rather than install the published package, clone the project and create a virtual environment.

### Windows setup

```powershell
git clone https://github.com/Pranesh0805-S/DevMate-finetuning.git
cd DevMate-finetuning

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The editable installation installs the client from the local checkout and the development dependencies defined in the project configuration.

### Build the Python package

```powershell
python -m pip install build
python -m build
```

This creates a wheel and source distribution in `dist/`. The package contains the Python client, not the base model or adapter weights.

For the pinned training environment, the repository also provides a `requirements.txt`. Follow the project configuration when installing the experiment dependencies.

## Testing and Code Quality

### Automated tests

Run the test suite from the repository root:

```powershell
python -m pytest -q tests/
```

**Latest recorded local result: 22 tests passed.**

The tests cover selected dataset, review CLI, and Python client validation behavior. Passing tests do not independently establish general model intelligence or response quality.

### Ruff

```powershell
python -m ruff check src tests
```

The configured Ruff checks passed locally. The `TRY004` rule is intentionally ignored in `pyproject.toml` to preserve the current validation exception behavior.

### Continuous integration

GitHub Actions runs automated checks on pushes and pull requests. The workflow installs project dependencies, runs Ruff, and executes the test suite.

See the [GitHub Actions workflow history](https://github.com/Pranesh0805-S/DevMate-finetuning/actions) for workflow results.

## Evaluation Results

The V3 evaluation compared four variants across 21 programming and developer-workflow questions. Answers were reviewed on a 1–5 scale for technical correctness, relevance, and practical usefulness, alongside a critical-error flag.

| Model | Correctness | Relevance | Usefulness | Critical errors | Combined score |
|---|---:|---:|---:|---:|---:|
| Base model | 67/105 | 100/105 | 67/105 | 11 | 74.29% |
| DevMate V1 | 76/105 | 99/105 | 74/105 | 7 | 79.05% |
| DevMate V2 | 79/105 | 90/105 | 58/105 | 4 | 72.06% |
| DevMate V3 | 80/105 | 90/105 | 61/105 | 2 | 73.33% |

### Interpretation

- V3 achieved the highest technical-correctness subtotal in this review.
- V3 had the fewest flagged critical errors.
- V1 achieved the highest combined score.
- V3's combined score was below both the base model and V1.

**These results do not demonstrate an overall improvement from fine-tuning.** The evaluation contains only 21 questions, relies on human ratings, and has semantic overlap between some evaluation topics and training examples. It is a development evaluation, not an independent benchmark. The ratings and audit notes have not been independently validated.

See [`docs/evaluation-v3.md`](docs/evaluation-v3.md) for the detailed report.

## Repository Structure

```text
DevMate-finetuning/
├── configs/                  # Training configuration
├── data/                     # Dataset files
├── docs/                     # Evaluation reports and documentation
├── docker/
│   └── app.py                # FastAPI application
├── examples/                 # Client usage examples
├── src/
│   ├── devmate/              # Python client package
│   └── ...                   # Training and evaluation scripts
├── tests/                    # Automated tests
├── results/                  # Local outputs and evaluation artifacts
├── .github/
│   └── workflows/            # GitHub Actions CI
├── Dockerfile                # Container image build
├── .dockerignore             # Docker build exclusions
├── pyproject.toml             # Package and Ruff configuration
├── requirements.txt          # Experiment environment
└── .gitignore
```

Generated outputs, model weights, and local review records may be excluded from Git. Check the relevant scripts and configuration before running workflows that depend on local artifacts.

## Training and Evaluation

The repository contains scripts for dataset preparation, fine-tuning, model evaluation, and scorecard generation. Inspect each script's configuration and input/output paths before running it.

Typical project commands include:

```powershell
python -m pytest -q tests/
python src/evaluate_model.py
python src/final_scorecard.py
```

The evaluation and scorecard commands require their expected input files to exist under `results/`. Follow the evaluation documentation and script configuration before running them.

## Limitations and Security

- DevMate is a small experimental model and may generate incorrect or misleading programming advice.
- CPU fine-tuning is relatively slow.
- The evaluation set is small and not independent of the training topics.
- Human-assigned ratings can be subjective.
- Automated tests validate selected software behavior, not general model intelligence.
- Model weights and evaluation artifacts may need to be generated locally.
- The Python client and Docker API require access to the private Hugging Face adapter repository.
- The HTTP API currently lacks application-level authentication and rate limiting.
- Successful testing in one environment does not guarantee compatibility with every dependency version or deployment configuration.

Do not use DevMate's output as a substitute for testing code, checking official documentation, or reviewing security-sensitive changes.

## Roadmap

- Improve dataset coverage and quality.
- Reduce overlap between training examples and evaluation questions.
- Build a separate held-out test set.
- Add repeatable evaluation procedures and stronger validation.
- Investigate V4 improvements using documented failure cases.
- Expand client and API automated tests.
- Add authentication and rate limiting before exposing the API beyond localhost.
- Continue reviewing dependency compatibility and licensing as the project evolves.

## License and Distribution

The repository's `LICENSE` file declares the MIT license for the project's original code and documentation, subject to the scope described in that file. This does **not** automatically grant rights to the dataset, adapter weights, base model, or third-party components.

The base model, dependencies, and training dataset may have separate license or usage terms. The dataset's provenance and redistribution permissions have not been fully verified.

Before making the adapter public or distributing additional artifacts, verify:

- The base model's license and adapter distribution requirements.
- Dataset permissions and redistribution restrictions.
- The intended license for DevMate-specific code and artifacts.
- Dependency licensing and package metadata.

Until those questions are resolved, the Hugging Face adapter should remain private.

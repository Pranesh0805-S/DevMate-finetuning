# DevMate --- Small LLM Fine-Tuning

An experimental developer-focused language model built by fine-tuning
**Qwen3-0.6B** with **Low-Rank Adaptation (LoRA)**.

DevMate explores how targeted training examples influence a small
language model's responses to programming questions and developer
workflows. The project combines parameter-efficient fine-tuning, dataset
preparation, structured evaluation, a Python client, automated testing,
and continuous integration.

> **Project status:** Experimental research project. Evaluation results
> are preliminary and do not establish general improvements across tasks
> or domains.

## Project Goals

-   Fine-tune a compact language model using LoRA.
-   Maintain a reproducible dataset preparation and training pipeline.
-   Compare the base model against successive DevMate versions.
-   Evaluate technical correctness, relevance, usefulness, and critical
    errors.
-   Provide a Python client for loading the adapter and generating
    responses.
-   Automate tests and code-quality checks through GitHub Actions.
-   Document limitations and use evaluation findings to guide future
    experiments.

## Technology Stack

  Component                Technology
  ------------------------ -------------------------------------------
  Base model               `Qwen/Qwen3-0.6B`
  Fine-tuning              Hugging Face Transformers and PEFT (LoRA)
  Dataset tooling          Hugging Face Datasets
  Training framework       PyTorch
  Programming language     Python
  Package build            setuptools and `pyproject.toml`
  Automated testing        pytest
  Linting                  Ruff
  Continuous integration   GitHub Actions
  Model hosting            Hugging Face

## Development Environment

The DevMate V3 training experiment was conducted using:

  Component            Configuration
  -------------------- -------------------
  Processor            AMD Ryzen 7 7730U
  Memory               16 GB RAM
  Operating system     Windows 11
  Python               3.12.10
  Training device      CPU
  Fine-tuning method   LoRA

## DevMate V3 Experiment

The V3 training run used:

-   58 training examples
-   2 training epochs
-   30 optimizer steps
-   Approximately 194.9 seconds of CPU training
-   2,293,760 trainable parameters out of 598,343,680 total parameters
-   Approximately 0.3834% trainable parameters

The reported training loss was 2.284, and evaluation loss reached 2.030
during the run. Loss values alone do not establish that generated
answers are more accurate or useful.

### Model access

The trained adapter is hosted in the [DevMate V3 Hugging Face
repository](https://huggingface.co/Pranesh0805-S/DevMate-V3).

**The adapter repository is currently private.** Users must have
permission to access it and authenticate with Hugging Face. The Python
package does not bundle the base model or adapter weights.

## Python Client

The published Python distribution is **`pranesh-devmate-toolkit`**,
version **`0.1.1`**. Its Python import name is `devmate`.

### Install from PyPI

``` bash
python -m pip install pranesh-devmate-toolkit
```

-   [View DevMate Toolkit on
    PyPI](https://pypi.org/project/pranesh-devmate-toolkit/)
-   [View version
    0.1.1](https://pypi.org/project/pranesh-devmate-toolkit/0.1.1/)

### Usage

``` python
from devmate import DevMate

model = DevMate()

answer = model.generate(
    "Explain Python functions with an example."
)

print(answer)
```

The client loads the Qwen3-0.6B base model and the DevMate V3 LoRA
adapter, then provides a `generate()` method for text generation.

The first initialization downloads required model files if they are not
already cached. Access to the private Hugging Face adapter is required;
installing the Python package alone does not grant access to the
adapter.

The client defaults to:

-   Base model: `Qwen/Qwen3-0.6B`
-   Adapter: `Pranesh0805-S/DevMate-V3`
-   Maximum generated tokens: 180
-   Device: CUDA when available, otherwise CPU
-   Base model precision: float32

Loading the model can consume substantial memory, and CPU generation may
be slow.

### Install from a local checkout

If you want to work on the repository itself, rather than install the
published package, clone the project and install it in editable mode:

``` powershell
git clone https://github.com/Pranesh0805-S/DevMate-finetuning.git
cd DevMate-finetuning

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The editable installation installs the client from the local checkout
and its development dependencies, including pytest and Ruff.

### Build the package

To build distribution files locally:

``` powershell
python -m pip install build
python -m build
```

The command creates a wheel and source distribution in `dist/`. The
wheel contains the Python client, not the Qwen base model or DevMate
adapter weights.

## Clean-Environment Verification

The published package was tested in a separate virtual environment,
independent of the original development environment.

Verified results:

-   Built the Python wheel successfully.
-   Uploaded the package to TestPyPI and installed it in a clean
    environment.
-   Published version `0.1.1` to PyPI.
-   Installed version `0.1.1` from the public PyPI index.
-   Verified that `from devmate import DevMate` succeeds.
-   Confirmed that automated tests and Ruff checks pass.

These checks verify the package installation and import path in the
tested environment. They do not guarantee compatibility with every
dependency version or establish general model answer quality.

## Testing and Code Quality

### Run automated tests

Run the test suite from the repository root:

``` powershell
python -m pytest -q tests/
```

**Latest recorded local result: 22 tests passed.**

The tests cover selected dataset, review CLI, and Python client
validation behavior. Passing tests does not independently validate the
model's general intelligence or evaluation ratings.

### Run Ruff

``` powershell
python -m ruff check src tests
```

The configured Ruff checks passed locally. The `TRY004` rule is
intentionally ignored in `pyproject.toml` to preserve the current
validation exception behavior.

### Continuous integration

GitHub Actions runs automated checks on pushes and pull requests. The
workflow installs project dependencies, runs Ruff, and executes the test
suite.

See the [GitHub Actions workflow
history](https://github.com/Pranesh0805-S/DevMate-finetuning/actions)
for run results.

## Evaluation Results

The V3 evaluation compared four variants across 21 programming and
developer-workflow questions. Answers were reviewed on a 1--5 scale for
technical correctness, relevance, and practical usefulness, alongside a
critical-error flag.

  ---------------------------------------------------------------------------
  Model       Correctness    Relevance   Usefulness     Critical     Combined
                                                          errors        score
  --------- ------------- ------------ ------------ ------------ ------------
  Base             67/105      100/105       67/105           11       74.29%
  model                                                          

  DevMate          76/105       99/105       74/105            7       79.05%
  V1                                                             

  DevMate          79/105       90/105       58/105            4       72.06%
  V2                                                             

  DevMate          80/105       90/105       61/105            2       73.33%
  V3                                                             
  ---------------------------------------------------------------------------

### Interpreting the results

-   V3 achieved the highest technical-correctness subtotal in this
    review.
-   V3 had the fewest flagged critical errors.
-   V1 achieved the highest combined score.
-   V3's combined score was below both the base model and V1.

**These results do not demonstrate an overall improvement from
fine-tuning.** The evaluation contains only 21 questions, relies on
human ratings, and has semantic overlap between some evaluation topics
and training examples. It is a development evaluation, not an
independent benchmark. The ratings and audit notes have not been
independently validated.

See [`docs/evaluation-v3.md`](docs/evaluation-v3.md) for the detailed
report.

## Repository Structure

``` text
DevMate-finetuning/
├── configs/                  # Training configuration
├── data/                     # Dataset files
├── docs/                     # Evaluation reports and documentation
├── examples/                 # Client usage examples
├── src/
│   ├── devmate/              # Python client package
│   └── ...                   # Training and evaluation scripts
├── tests/                    # Automated tests
├── results/                  # Local outputs and evaluation artifacts
├── .github/
│   └── workflows/            # GitHub Actions CI
├── pyproject.toml            # Package and Ruff configuration
├── requirements.txt          # Pinned experiment environment
└── .gitignore
```

Generated outputs, model weights, and local review records may be
excluded from Git. Check the relevant scripts and configuration before
running workflows that depend on local artifacts.

## Setup on Windows

For repository development, use the local-checkout instructions above.
The repository provides a pinned `requirements.txt` for the experiment
environment and a `pyproject.toml` for the installable Python client.

To install the pinned experiment environment and client development
tools:

``` powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e ".[dev]"
```

The requirements file includes CPU-only PyTorch. Training speed and
compatibility depend on Python, installed packages, available memory,
and hardware.

Run the tests and code-quality checks:

``` powershell
python -m pytest -q tests/
python -m ruff check src tests
```

The client usage example loads the model, so run it separately when you
want to perform inference and have access to the private adapter
repository.

## Training and Evaluation

The repository contains scripts for dataset preparation, fine-tuning,
model evaluation, and scorecard generation. Inspect each script's
configuration and input/output paths before running it. Some workflows
require locally generated files or review data that are not tracked in
Git.

Typical project commands include:

``` powershell
python -m pytest -q tests/
python src/evaluate_model.py
python src/final_scorecard.py
```

The evaluation and scorecard commands require their expected input files
to exist under `results/`. Follow the evaluation documentation and
script configuration before running them.

## Limitations

-   DevMate is a small experimental model and may generate incorrect or
    misleading programming advice.
-   CPU fine-tuning is relatively slow.
-   The evaluation set is small and not independent of the training
    topics.
-   Human-assigned ratings can be subjective.
-   Automated tests validate selected software behavior, not general
    model intelligence.
-   Model weights and evaluation artifacts may need to be generated
    locally.
-   The Python client currently depends on access to the private Hugging
    Face adapter repository.
-   Successful testing in one clean environment does not guarantee
    compatibility with every dependency version.

Do not use DevMate's output as a substitute for testing code, checking
official documentation, or reviewing security-sensitive changes.

## Roadmap

-   Improve dataset coverage and quality.
-   Reduce overlap between training examples and evaluation questions.
-   Build a separate held-out test set.
-   Add repeatable evaluation procedures and stronger validation.
-   Investigate V4 improvements using documented failure cases.
-   Expand client-specific automated tests.
-   Continue reviewing dependency compatibility and licensing as the
    project evolves.

## License and Distribution

The repository's `LICENSE` file declares the MIT license for the
project's original code and documentation, subject to the scope
described in that file. This does **not** automatically grant rights to
the dataset, adapter weights, base model, or third-party components.

The base model, dependencies, and training dataset may have separate
license or usage terms. The dataset's provenance and redistribution
permissions have not been fully verified.

Before making the adapter public or distributing additional artifacts,
verify:

-   The base model's license and adapter distribution requirements.
-   Dataset permissions and redistribution restrictions.
-   The intended license for DevMate-specific code and artifacts.
-   Dependency licensing and package metadata.

Until the adapter and dataset redistribution questions are resolved, the
Hugging Face adapter should remain private.

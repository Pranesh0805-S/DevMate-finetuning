# DevMate Dataset

This directory contains the datasets used to develop and evaluate DevMate, a small language model fine-tuning experiment focused on developer assistance.

## Dataset goals

- Teach clear, concise programming explanations.
- Provide practical code examples.
- Explain common debugging and Git workflows.
- Encourage accurate answers and explicit uncertainty when necessary.

## Data format

Dataset examples will use JSON Lines (`.jsonl`) with one JSON object per line.

Each example will contain:

- `messages`: a list of conversational messages.
- `role`: the speaker, such as `user` or `assistant`.
- `content`: the text of the message.

Example:

```json
{"messages":[{"role":"user","content":"What is a Python function?"},{"role":"assistant","content":"A Python function is a reusable block of code defined with the def keyword."}]}
```

## Quality and evaluation

Training and evaluation examples must be kept separate. Evaluation examples must not be included in the training data. Examples should be reviewed for correctness, clarity, and usefulness.

## Model and dataset licensing

Record the source and license of any external dataset used. Prefer original, manually reviewed examples for the initial experiment. Do not include secrets, private information, or copyrighted datasets without appropriate permission.

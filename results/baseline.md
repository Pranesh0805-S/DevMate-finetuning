# DevMate Baseline Evaluation

## Model
- Base model: Qwen/Qwen3-0.6B
- Inference device: CPU
- Framework: PyTorch and Transformers
- Fine-tuning status: Not fine-tuned

## Test 1: Explain a Python Function

### Prompt
Explain what a Python function is in simple terms. Give one short code example.

### Observed Result
The model explained that a function is a reusable block of code, described parameters and return values, and provided a valid `add_numbers(a, b)` example.

### Initial Assessment
- Basic explanation: Successful
- Code example: Appropriate
- Readability: Good
- Baseline recorded: Yes

## Limitations
This is one qualitative test, not a comprehensive benchmark. It does not establish that fine-tuning improves the model.

## Next Steps
1. Prepare a curated developer-focused dataset.
2. Separate training examples from evaluation examples.
3. Fine-tune using LoRA.
4. Evaluate the base and fine-tuned models using the same prompts.

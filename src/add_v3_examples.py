import json
from pathlib import Path

TRAIN_FILE = Path("data/train.jsonl")
BACKUP_FILE = Path("data/train.before-v3.jsonl")

examples = [
    {
        "question": "How do I print a Python exception traceback?",
        "answer": "Use traceback.print_exc() inside an except block to print the active exception traceback. Example:\n\nimport traceback\n\ntry:\n    result = 10 / 0\nexcept Exception:\n    traceback.print_exc()\n\nDo not call sys.exit() before printing the traceback, because the later statement will never execute."
    },
    {
        "question": "What causes an IndexError when accessing a Python list?",
        "answer": "An IndexError occurs when a list index is outside the valid range. For a list of length n, valid positive indices range from 0 to n - 1. An empty list has no valid indices. Check the list length before indexing, or iterate over the list directly. Example: items = [10, 20]; print(items[1]) returns 20."
    },
    {
        "question": "What is the difference between KeyError and IndexError in Python?",
        "answer": "KeyError commonly occurs when accessing a dictionary with a key that does not exist, such as data['missing']. IndexError occurs when accessing a sequence with an invalid index, such as items[5] when the list is shorter. For dictionaries, use data.get('key') when a missing key should return a default value."
    },
    {
        "question": "Write a Python function that returns the largest number in a list without using max(), including negative numbers.",
        "answer": "Initialize the largest value from the first list element rather than zero, so lists containing only negative numbers work. Handle an empty list explicitly:\n\ndef largest_number(numbers):\n    if not numbers:\n        raise ValueError('numbers must not be empty')\n    largest = numbers[0]\n    for number in numbers[1:]:\n        if number > largest:\n            largest = number\n    return largest\n\nExample: largest_number([-8, -3, -10]) returns -3."
    },
    {
        "question": "Why does a Python function return None when I expect a value?",
        "answer": "A Python function returns None implicitly if execution reaches the end without a return statement. Make sure the function returns the intended value and that the return statement is reached. Example:\n\ndef add(a, b):\n    return a + b\n\nresult = add(2, 3)  # 5\n\nCalling print() inside a function does not return the printed value."
    },
    {
        "question": "How do I export installed Python packages to requirements.txt?",
        "answer": "Activate the intended virtual environment, then run python -m pip freeze > requirements.txt. This writes the environment's installed package versions to the file. To install them later, run python -m pip install -r requirements.txt. Review the file before sharing it, because it may include packages you do not want to distribute."
    },
    {
        "question": "How can I check whether a Python package is installed in the active environment?",
        "answer": "Use python -m pip show package_name to inspect a specific package, replacing package_name with the package's distribution name. Use python -m pip list to list installed packages. Running python -m pip ensures pip is associated with the selected Python interpreter. If the package is not found, verify that the correct virtual environment is active."
    },
    {
        "question": "I committed changes on the wrong Git branch. How can I recover safely?",
        "answer": "First run git status and git log --oneline -5 to inspect your working tree and recent commits. Do not delete branches or reset history before confirming where the changes are and whether the commit was pushed. If the commit is local and the changes need to move, create or switch to the intended branch and use a carefully chosen cherry-pick or branch-based recovery. Preserve a backup branch before rewriting history, and choose the exact steps based on the current branch, target branch, and working-tree state."
    },
    {
        "question": "What is the safest way to undo a Git commit that has already been pushed?",
        "answer": "For a commit on a shared branch, git revert <commit-hash> is usually the safest approach because it creates a new commit that reverses the selected commit's changes without rewriting existing history. Inspect the commit first with git show <commit-hash>. Avoid git reset followed by a force push on shared branches unless you understand the consequences and coordinate with collaborators."
    },
    {
        "question": "How can Python read API keys without hardcoding them in source code?",
        "answer": "Store the API key in an environment variable and read it with os.environ or os.getenv. Example:\n\nimport os\n\napi_key = os.getenv('MY_API_KEY')\nif not api_key:\n    raise RuntimeError('MY_API_KEY is not configured')\n\nSet the variable in your operating system or development environment. Do not commit real secrets to Git. A .env file used locally should be excluded from version control, and production secrets should use an appropriate secrets manager."
    }
]

def read_jsonl(path):
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]

if not TRAIN_FILE.exists():
    raise SystemExit(f"Missing training file: {TRAIN_FILE}")

if not BACKUP_FILE.exists():
    raise SystemExit(f"Missing backup file: {BACKUP_FILE}")

original = read_jsonl(TRAIN_FILE)
backup = read_jsonl(BACKUP_FILE)

if len(original) != 50 or len(backup) != 50:
    raise SystemExit(
        f"Expected 50 original and backup examples; found "
        f"{len(original)} and {len(backup)}. No changes made."
    )

def get_question(record):
    for message in record.get("messages", []):
        if message.get("role") == "user":
            return message.get("content", "").strip().casefold()
    return ""

existing_questions = {get_question(record) for record in original}
additions = []

for example in examples:
    question = example["question"]
    if question.strip().casefold() in existing_questions:
        print(f"SKIP duplicate: {question}")
        continue

    additions.append({
        "messages": [
            {"role": "user", "content": question},
            {"role": "assistant", "content": example["answer"]}
        ]
    })
    existing_questions.add(question.strip().casefold())

candidate = original + additions

for index, record in enumerate(candidate, start=1):
    if not isinstance(record.get("messages"), list):
        raise SystemExit(f"Record {index} has invalid messages. No changes made.")
    if not any(m.get("role") == "user" for m in record["messages"]):
        raise SystemExit(f"Record {index} has no user message. No changes made.")
    if not any(m.get("role") == "assistant" for m in record["messages"]):
        raise SystemExit(f"Record {index} has no assistant message. No changes made.")

# Write to a separate file first so the current dataset remains intact on failure.
temporary = TRAIN_FILE.with_suffix(".v3-tmp.jsonl")
with temporary.open("w", encoding="utf-8", newline="\n") as file:
    for record in candidate:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

# Verify the temporary JSONL before replacing the training file.
verified = read_jsonl(temporary)
if len(verified) != len(candidate):
    temporary.unlink(missing_ok=True)
    raise SystemExit("Verification failed. Original training file unchanged.")

TRAIN_FILE.write_text(
    "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in verified),
    encoding="utf-8"
)
temporary.unlink(missing_ok=True)

print(f"Original examples: {len(original)}")
print(f"New examples added: {len(additions)}")
print(f"Total training examples: {len(verified)}")
print("Backup remains unchanged: data/train.before-v3.jsonl")

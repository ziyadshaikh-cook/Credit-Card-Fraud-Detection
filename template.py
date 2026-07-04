import os
from pathlib import Path

folders = [
    "data/raw",
    "data/processed",
    "notebook",
    "src",
]

files = [
    "src/utils.py",
    "notebook/01_eda.ipynb",
    "notebook/02_supervised_model.ipynb",
    "notebook/03_anomaly_detection.ipynb",
    "notebook/04_cost_sensitive_eval.ipynb",
    "requirements.txt",
    "README.md",
    ".gitignore",
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    path = Path(file)
    if not path.exists():
        path.touch()
        print(f"Created: {file}")
    else:
        print(f"Already exists: {file}")

print("\nScaffolding complete.")

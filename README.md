# PEFT-Merging

Professional utilities for working with PEFT adapters and fine-tuned models — focused on practical, reproducible workflows for training, merging, inspecting, and running adapter-based models.

This repository contains utilities and scripts to help train and manage parameter-efficient fine-tuning (PEFT) adapters, keep project artifacts tidy, inspect adapter artifacts, and run predictions using fine-tuned models. The project is structured for clarity and reproducibility, suitable for demonstration in a portfolio or client deliverable.

---

Table of Contents
- Overview
- Key Features
- Tech Stack
- Quick Start
- Common Workflows
  - Project Cleanup
  - Using a Fine-tuned Model
  - Troubleshooting
- Project Structure
- Role & Outcomes 
- Contributing
- License & Contact

---

Overview
This repo provides a lightweight, practical toolkit for handling PEFT-style adapters with Hugging Face / PyTorch models, including scripts to:
- Clean up temporary and redundant files from experiments
- Inspect adapter files and metadata
- Run inference using fine-tuned adapters (interactive and scripted)
- Provide basic troubleshooting utilities to help recover or debug adapter loading problems

Key Features
- Cleanup utilities to keep your experiment directories neat and conflict-free
- Convenience script to inspect and test adapter files interactively
- Prediction script for quick classification / inference using your fine-tuned model
- Small troubleshooting helpers to diagnose or fix adapter loading issues

Tech Stack
- Python 3.8+
- PyTorch
- Hugging Face Transformers
- PEFT (parameter-efficient fine-tuning) tools
- Standard CLI scripts and small utilities for common workflows

Quick Start

1. Clone the repository
```bash
git clone https://github.com/HarshXAI/PEFT-Merging.git
cd PEFT-Merging
```

2. Create a virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```
(If you don't have a requirements file, install typical packages:)
```bash
pip install torch transformers accelerate peft
```

Common Workflows

Project Cleanup
To list potentially unwanted files (dry-run):
```bash
python cleanup.py
```
To actually remove the identified files:
```bash
python cleanup.py --execute
```
Cleanup will identify common items such as:
- Redundant or conflicting training scripts
- Temporary and cache files (.pt, .ckpt, __pycache__, large logs)
- Outdated test files or artifacts

Using Your Fine-tuned Model

Option 1 — Interactive convenience script
```bash
chmod +x use_finetuned_model.sh
./use_finetuned_model.sh
```
This script guides you through:
- Inspecting available adapter files
- Running quick tests on example inputs
- Classifying or scoring your own inputs interactively

Option 2 — Direct prediction script
```bash
# Run the default example prediction
python peft_email_predictor.py

# Predict a specific string
python peft_email_predictor.py --email "Dear user, your account has been compromised..."

# Predict using a file with the email text
python peft_email_predictor.py --file /path/to/email.txt

# Increase output detail for debugging
python peft_email_predictor.py --verbose

# Example: change precision if there are loading/precision issues
python peft_email_predictor.py --precision float16
```

Troubleshooting
If you encounter issues:
1. Inspect adapter files
```bash
python adapter_inspector.py
```
2. Attempt to fix adapter loading issues (dry-run)
```bash
python fix_adapter_loading.py --test
```
3. Try alternate precisions or model configurations (e.g., float16 vs float32)

Project Structure (high level)
- cleanup.py                  — cleanup utility to find and remove artifact files
- peft_email_predictor.py     — example prediction script for fine-tuned models
- use_finetuned_model.sh      — convenience wrapper for interactive testing
- adapter_inspector.py        — inspect adapter metadata and files
- fix_adapter_loading.py      — helper to attempt fixes for adapter loading
- README.md                   — this document
- requirements.txt            — (optional) Python dependencies

Role & Outcomes (for your Upwork portfolio)
- Role: Solo developer / maintainer
- Activities: Designed and developed utilities to maintain reproducible PEFT workflows, created scripts to inspect, run and debug adapter-based models, and implemented cleanup utilities to streamline experimentation.
- Outcomes: Reduced friction during model iteration and debugging; made it straightforward to validate and deploy adapter-based fine-tuned models for classification tasks.
- Value to clients: Faster experimentation cycles, lower risk of model/adapter mismatch, and reproducible scripts that can be integrated into existing ML pipelines.

How to Present this Project on Upwork
- Short blurb: "PEFT-Merging — utilities for managing, validating, and running PEFT adapters (Hugging Face). Implemented cleanup, inspection, and prediction scripts for reproducible fine-tuning workflows."
- Bullet points to highlight: tech stack (PyTorch, Transformers, PEFT), tasks performed (utilities for training artifacts, inference tooling, debugging helpers), and impact (reduced manual overhead, reproducible results).
- Link to repo and a 1–2 minute summary video or screenshots (optional but recommended).

Contributing
Contributions are welcome. If you'd like to contribute:
- Open an issue describing the change
- Create a branch, push a PR with tests or a short demo of the change

License & Contact
- License: MIT (or change to your preferred license)
- Contact: https://github.com/HarshXAI


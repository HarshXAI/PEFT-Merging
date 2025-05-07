// ...existing code...

## Project Cleanup

To keep the project organized, you can use the cleanup script to identify and remove unwanted files:

```bash
# List unwanted files (dry run)
python cleanup.py

# Remove unwanted files
python cleanup.py --execute
```

The cleanup script will handle:
- Redundant or conflicting training scripts
- Temporary and cache files
- Outdated test files
- Log files and other large unnecessary files

This helps maintain a clean project structure and avoids conflicts between different approaches.

## Using Your Fine-tuned Phishing Detection Model

Once you have trained your model, you can use it to classify emails:

### Option 1: Using the convenience script

```bash
# Make the script executable
chmod +x use_finetuned_model.sh

# Run the script
./use_finetuned_model.sh
```

This interactive script will guide you through:
- Inspecting your adapter files
- Testing with example emails
- Classifying your own emails

### Option 2: Using the prediction script directly

```bash
# Predict with an example email
python peft_email_predictor.py

# Predict with a specific email
python peft_email_predictor.py --email "Dear user, your account has been compromised..."

# Predict with an email file
python peft_email_predictor.py --file /path/to/email.txt

# Get more detailed output
python peft_email_predictor.py --verbose
```

### Troubleshooting

If you encounter issues with your fine-tuned model:

1. Inspect the adapter files:
```bash
python adapter_inspector.py
```

2. Try fixing adapter loading issues:
```bash
python fix_adapter_loading.py --test
```

3. Try a different precision:
```bash
python peft_email_predictor.py --precision float16
```

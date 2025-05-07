#!/bin/bash

echo "🚀 Using Fine-tuned Phishing Detection Model"
echo "==========================================="
echo ""

# Activate virtual environment
source .venv/bin/activate 2>/dev/null || echo "⚠️ Virtual environment not activated, using system Python."

# Check for required packages
PACKAGES="transformers peft torch safetensors"
for package in $PACKAGES; do
    python -c "import $package" 2>/dev/null || {
        echo "📦 Installing missing package: $package"
        pip install $package
    }
done

# Check if adapter directory exists
ADAPTER_DIR="/Users/harshkanani/Desktop/synergy/phishing_finetuned_model"
if [ ! -d "$ADAPTER_DIR" ]; then
    echo "❌ Adapter directory not found: $ADAPTER_DIR"
    exit 1
fi

echo "📂 Using adapter from: $ADAPTER_DIR"
echo ""
echo "Select an option:"
echo "1) Inspect adapter files"
echo "2) Run adapter with example emails"
echo "3) Check a specific email"
echo "4) Exit"

read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        # Inspect adapter
        echo "🔍 Inspecting adapter files..."
        python adapter_inspector.py
        ;;
    2)
        # Run with example emails
        echo "🧪 Testing with example emails..."
        python peft_email_predictor.py
        ;;
    3)
        # Check specific email
        read -p "Enter email text or path to email file: " email_input
        
        # Check if input is a file
        if [ -f "$email_input" ]; then
            python peft_email_predictor.py --file "$email_input" --verbose
        else
            python peft_email_predictor.py --email "$email_input" --verbose
        fi
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

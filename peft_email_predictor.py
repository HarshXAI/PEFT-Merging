import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import argparse
import os
import sys
import json

def load_peft_model(adapter_path):
    """
    Load a PEFT model with adapters for phishing detection.
    
    Args:
        adapter_path: Path to the adapter files
        
    Returns:
        model, tokenizer: The loaded model and tokenizer
    """
    try:
        # Load adapter config
        peft_config = PeftConfig.from_pretrained(adapter_path)
        print(f"Base model: {peft_config.base_model_name_or_path}")
        
        # Load base model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(peft_config.base_model_name_or_path)
        model = AutoModelForCausalLM.from_pretrained(
            peft_config.base_model_name_or_path,
            torch_dtype=torch.float32,  # Use float32 for CPU
            device_map="auto"
        )
        
        # Load adapter weights
        model = PeftModel.from_pretrained(model, adapter_path)
        
        print("✅ Model and adapter loaded successfully!")
        return model, tokenizer
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None

def predict_email(email_text, model, tokenizer, verbose=False):
    """
    Predict if an email is phishing or legitimate.
    
    Args:
        email_text: The email text to classify
        model: The PEFT model
        tokenizer: The tokenizer
        verbose: Whether to print verbose output
        
    Returns:
        dict: Prediction results
    """
    # Format the prompt for the model
    prompt = f"Classify if this email is phishing or legitimate.\n\nEmail: {email_text}\n\nClassification:"
    
    if verbose:
        print(f"Prompt: {prompt[:100]}...")
    
    # Generate prediction
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=50,
            temperature=0.1,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the generated output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the generated response (after the prompt)
    response = generated_text[len(prompt):].strip()
    
    # Determine classification based on the response
    is_phishing = "phishing" in response.lower() or "scam" in response.lower() or "fraud" in response.lower()
    is_legitimate = "legitimate" in response.lower() or "safe" in response.lower() or "genuine" in response.lower()
    
    # If model is confused or gives unclear answer
    if not (is_phishing or is_legitimate):
        # Default to suspicious if unclear
        is_phishing = True
    
    # Confidence level is approximate since LLMs don't give explicit probabilities
    confidence = 0.9 if is_phishing != is_legitimate else 0.6
    
    return {
        "is_phishing": is_phishing,
        "prediction": "PHISHING" if is_phishing else "LEGITIMATE",
        "confidence": confidence * 100,
        "full_response": response,
    }

def main():
    parser = argparse.ArgumentParser(description="Detect phishing emails using PEFT-fine-tuned language model")
    parser.add_argument("--email", type=str, help="Email text to analyze")
    parser.add_argument("--file", type=str, help="Path to file containing email text")
    parser.add_argument("--model", type=str, default="/Users/harshkanani/Desktop/synergy/phishing_finetuned_model", 
                       help="Path to adapter directory")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("--base-model", type=str, help="Override base model specified in adapter config")
    
    args = parser.parse_args()
    
    # Load model
    model_path = args.model
    if not os.path.exists(model_path):
        print(f"❌ Model path not found: {model_path}")
        sys.exit(1)
    
    try:
        # Check if adapter config exists
        config_path = os.path.join(model_path, "adapter_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                base_model = args.base_model or config.get('base_model_name_or_path')
                print(f"📄 Using base model: {base_model}")
        else:
            print(f"❌ adapter_config.json not found in {model_path}")
            if args.base_model:
                base_model = args.base_model
                print(f"📄 Using provided base model: {base_model}")
            else:
                print("❌ No base model specified. Please use --base-model")
                sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading adapter config: {e}")
        if args.base_model:
            base_model = args.base_model
            print(f"📄 Using provided base model: {base_model}")
        else:
            print("❌ Please specify base model with --base-model")
            sys.exit(1)
    
    model, tokenizer = load_peft_model(model_path)
    if model is None or tokenizer is None:
        sys.exit(1)
    
    # Get email text
    email_text = None
    if args.email:
        email_text = args.email
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                email_text = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
    else:
        # No email provided - use examples
        print("No email provided. Using example emails...")
        
        example_emails = [
            "Dear user, your account has been compromised. Click here immediately to secure your account: http://malicious-link.com",
            "Hi team, here's the agenda for tomorrow's meeting. Let me know if you have questions."
        ]
        
        for i, email in enumerate(example_emails):
            print(f"\n=== Example {i+1} ===")
            result = predict_email(email, model, tokenizer, args.verbose)
            
            print(f"Email: {email[:100]}..." if len(email) > 100 else f"Email: {email}")
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.1f}%")
            if args.verbose:
                print(f"Model response: {result['full_response']}")
        
        return
    
    # Make prediction
    result = predict_email(email_text, model, tokenizer, args.verbose)
    
    # Print results
    print("\n" + "="*60)
    print("PHISHING EMAIL DETECTION RESULTS")
    print("="*60)
    print(f"PREDICTION: {result['prediction']}")
    print(f"CONFIDENCE: {result['confidence']:.1f}%")
    
    if args.verbose:
        print("-"*60)
        print(f"Model response: {result['full_response']}")
    
    print("-"*60)
    email_preview = email_text[:200] + ("..." if len(email_text) > 200 else "")
    print(f"Email: {email_preview}")
    print("="*60)

if __name__ == "__main__":
    main()

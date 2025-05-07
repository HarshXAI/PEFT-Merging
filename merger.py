from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# 🔹 Use the base model you originally fine-tuned (update this to your actual base model)
base_model_name = "NousResearch/Llama-2-7b-chat-hf"  

# 🔹 Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype="auto",
    device_map="cpu"  # Change to "auto" if using GPU
)

# 🔹 Load LoRA adapter weights
lora_model = PeftModel.from_pretrained(base_model, "/Users/harshkanani/Desktop/synergy/phishing_finetuned_model")

# 🔹 Merge LoRA weights with the base model
merged_model = lora_model.merge_and_unload()

# 🔹 Save the fully merged model (now self-contained)
merged_model.save_pretrained("phishing_finetuned_complete")
AutoTokenizer.from_pretrained(base_model_name).save_pretrained("phishing_finetuned_complete")

print("✅ Model and tokenizer saved successfully!")
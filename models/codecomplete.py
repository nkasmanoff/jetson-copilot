# given an input string, generate completed output

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class CodeCompletionModel():
    def __init__(self, model_name, load_in_8bit=True):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, load_in_8bit=load_in_8bit)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()

    def complete(self, input_string):
        vibe_check_input = tokenizer(input_string, return_tensors="pt")

        with torch.no_grad():
            inputs = {k: v.to(device) for k, v in vibe_check_input.items()}
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=256,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                bos_token_id=tokenizer.bos_token_id
            )

            return tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]

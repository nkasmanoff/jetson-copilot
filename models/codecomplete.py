# given an input string, generate completed output

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('HUGGINGFACE_TOKEN')


class CodeCompletionModel():
    def __init__(self, model_name, load_in_8bit=True):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name,
                                                       token=access_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, load_in_8bit=load_in_8bit, token=access_token)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # self.model.to(self.device)
        self.model.eval()

    def complete(self, input_string):
        _input = self.tokenizer(input_string, return_tensors="pt")

        with torch.no_grad():
            inputs = {k: v.to(self.device)
                      for k, v in _input.items()}
            outputs = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=256,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id
            )

            return self.tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]


if __name__ == '__main__':
    code_model = CodeCompletionModel(model_name='bigcode/starcoderbase-1b')
    input_string = '# print hello world as a class'
    print(code_model.complete(input_string))

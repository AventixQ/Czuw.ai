import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('HF_TOKEN')

device = "cpu"
model_name = "speakleash/Bielik-11B-v2.3-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
model = model.half()

messages = [
    {"role": "system", "content": "Odpowiadaj krótko, precyzyjnie i wyłącznie w języku polskim."},
    {"role": "user", "content": "Jakie mamy pory roku w Polsce?"},
    {"role": "assistant", "content": "W Polsce mamy 4 pory roku: wiosna, lato, jesień i zima."},
    {"role": "user", "content": "Która jest najcieplejsza?"}
]

input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt")

model_inputs = input_ids.to(device)
model.to(device)

generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])
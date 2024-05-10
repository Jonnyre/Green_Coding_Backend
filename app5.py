import transformers
import torch
import os

os.environ["HF_TOKEN"] = ""
model_id = "meta-llama/Meta-Llama-3-8B"

pipeline = transformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")
print(pipeline("Hey how are you doing today?"))

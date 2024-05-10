import torch
import transformers
import os



model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
os.environ["HF_TOKEN"] = ""

pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",   
)

def chat_function(message, history, system_prompt,max_new_tokens,temperature):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]
    prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    temp = temperature + 0.1
    outputs = pipeline(
        prompt,
        max_new_tokens=max_new_tokens,
        eos_token_id=terminators,
        do_sample=True,
        temperature=temp,
        top_p=0.9,
    )
    return outputs[0]["generated_text"][len(prompt):]

if __name__ == "__main__":
    chat_function()
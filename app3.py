import torch
import transformers
import os

from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["HF_TOKEN"] = ""
model_name = "meta-llama/Meta-Llama-3-8B"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cpu",
)

def chat_function(system_prompt, user_messages, max_new_tokens, temperature):
    messages = [{"role": "system", "content": system_prompt}]
    for idx, message in enumerate(user_messages):
        messages.append({"role": "user", "content": message})
        if idx < len(user_messages) - 1:
            messages.append({"role": "assistant", "content": ""})  # Placeholder for assistant responses
    prompt = pipeline.tokenizer.chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("")
    ]
    temp = temperature + 0.1
    outputs = pipeline(
        prompt,
        max_new_tokens=max_new_tokens,
        eos_token_id=terminators[0],  # Use the EOS token ID
        do_sample=True,
        temperature=temp,
        top_p=0.9,
    )
    return outputs[0]["generated_text"][len(prompt):]

def console_chat():
    print("Welcome to Console Chat with Meta-Llama-3-8B-Instruct!")
    print("Enter 'exit' to end the conversation.")
    while True:
        system_prompt = input("System: ")
        if system_prompt.lower() == 'exit':
            print("Goodbye!")
            break
        user_messages = []
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'assistant':
                break
            user_messages.append(user_input)
        max_tokens = int(input("Max Tokens: "))
        temperature = float(input("Temperature: "))
        response = chat_function(system_prompt, user_messages, max_tokens, temperature)
        print("Llama:", response)

console_chat()

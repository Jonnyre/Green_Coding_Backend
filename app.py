import torch
import transformers
import os



model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
os.environ["HF_TOKEN"] = "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"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",   
)

pipeline.tokenizer.chat_template = {
    "user": "{{{message}}}",
    "system": "{{{response}}}",
}

def chat_with_model():
    print("Welcome to the Meta-Llama-3-8B-Instruct chat!")
    print("You can start typing your messages. Type 'quit' to exit.")

    while True:
        message = input("You: ")
        if message.lower() == "quit":
            print("Exiting chat.")
            break
        
        response = generate_response(message)
        print("Meta-Llama-3-8B-Instruct:", response)

def generate_response(message, max_new_tokens=50, temperature=0.7):
    temp = temperature + 0.1
    outputs = pipeline(
        message,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temp,
        top_p=0.9,
    )
    return outputs[0]["generated_text"][len(outputs):]

if __name__ == "__main__":
    chat_with_model()

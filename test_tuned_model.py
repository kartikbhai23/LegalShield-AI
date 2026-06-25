from unsloth import FastLanguageModel
import torch

# 1. Load the model and adapters
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "gemma4_tnc_lora", # The folder from your tree
    max_seq_length = 2048,
    load_in_4bit = True,
)

tokenizer.padding_side = "right"
tokenizer.pad_token = tokenizer.eos_token

FastLanguageModel.for_inference(model) # 2x faster inference

# 2. Test Input
input_text = "I, the user, hereby grant full legal permission to GlobalTech Inc. to access, store, and utilize my personal data, including but not limited to financial records and private communications, for the duration of my subscription and for a period of ten (10) years post-termination. This authorization is unconditional and irrevocable, superseding any prior privacy agreements or statutory rights to data protection. Furthermore, I acknowledge and accept that GlobalTech Inc. reserves the right to modify these terms without prior notification, and that my continued use of the service constitutes acceptance of such modifications."

# 3. Format using the chat template
messages = [
    {"role": "system", "content": "Summarize the following Terms and Conditions into 5 key points, highlight what to keep in mind, and provide a final recommendation."},
    {"role": "user", "content": input_text}
]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")

# 4. Generate
outputs = model.generate(input_ids=inputs, max_new_tokens=500)
response = tokenizer.batch_decode(outputs[:, inputs.shape[1]:], skip_special_tokens=True)[0]

print(response)
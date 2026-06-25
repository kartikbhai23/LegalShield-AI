import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import streamlit as st
from unsloth import FastLanguageModel
import torch
import time

st.set_page_config(page_title="LegalShield AI", page_icon="🛡️", layout="wide")

# Custom CSS for the colored decisions
st.markdown("""
    <style>
    .green-text { color: #22c55e; font-weight: bold; padding: 2px 4px; border-radius: 4px; border: 1px solid #22c55e; }
    .yellow-text { color: #eab308; font-weight: bold; padding: 2px 4px; border-radius: 4px; border: 1px solid #eab308; }
    .red-text { color: #ef4444; font-weight: bold; padding: 2px 4px; border-radius: 4px; border: 1px solid #ef4444; }
    .metrics { color: #94a3b8; font-size: 0.8rem; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    # Force VRAM cleanup
    torch.cuda.empty_cache()
    
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "gemma4_tnc_lora", 
        max_seq_length = 512,  # Optimized for 4GB VRAM
        load_in_4bit = True,
        local_files_only = True,
        device_map = {"": 0}
    )
    tokenizer.padding_side = "right"
    tokenizer.pad_token = tokenizer.eos_token
    FastLanguageModel.for_inference(model)
    return model, tokenizer

model, tokenizer = load_model()

st.title("🛡️ LegalShield: AI T&C Auditor")

col1, col2 = st.columns([1, 1])

with col1:
    tc_input = st.text_area("Paste Terms and Conditions here:", height=400, placeholder="Drop legal text here...")
    analyze_btn = st.button("Start Audit", use_container_width=True)

with col2:
    if analyze_btn and tc_input:
        # STAGE 1: Internal Logs (Preparation)
        with st.status("System Check...", expanded=True) as status:
            st.write("Checking VRAM availability...")
            torch.cuda.empty_cache()
            
            st.write("Encoding input tokens...")
            messages = [
                {"role": "system", "content": "Summarize the following Terms and Conditions into 5 key points, highlight what to keep in mind, and provide a final recommendation."},
                {"role": "user", "content": tc_input}
            ]
            inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
            
            st.write("Ready for inference.")
            status.update(label="Initialization Complete", state="complete", expanded=False)

        # STAGE 2: Thinking & Generating Spinner
        # This spinner stays visible ONLY while the GPU is processing
        with st.spinner("🧠 Thinking and Generating Summary..."):
            start_time = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    input_ids=inputs, 
                    max_new_tokens=512, 
                    use_cache=True,
                    temperature=0.1
                )
            end_time = time.time()

        # Spinner disappears here automatically!
        
        # STAGE 3: Streaming Output to User
        st.markdown("### Analysis Result")
        output_placeholder = st.empty()
        
        # Performance Data
        duration = end_time - start_time
        raw_text = tokenizer.batch_decode(outputs[:, inputs.shape[1]:], skip_special_tokens=True)[0]
        token_count = len(outputs[0]) - len(inputs[0])
        tps = token_count / duration

        # Stream text with color highlights
        full_response = ""
        words = raw_text.split(" ")
        for i in range(len(words)):
            full_response = " ".join(words[:i+1])
            
            # Apply Colors
            display_text = full_response.replace("ACCEPT", '<span class="green-text">ACCEPT</span>')
            display_text = display_text.replace("PROCEED WITH CAUTION", '<span class="yellow-text">PROCEED WITH CAUTION</span>')
            display_text = display_text.replace("DECLINE", '<span class="red-text">DECLINE</span>')
            
            output_placeholder.markdown(display_text, unsafe_allow_html=True)
            time.sleep(0.01) # Smooth streaming speed

        # Final Metrics
        st.markdown(f"""
        <div class="metrics">
        🚀 {tps:.2f} tokens/sec | ⏱️ {duration:.2f}s | 💾 {torch.cuda.max_memory_allocated() / 1024**3:.2f} GB VRAM used
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("Input a document to begin the AI audit.")
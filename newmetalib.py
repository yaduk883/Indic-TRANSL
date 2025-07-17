import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Title
st.title("🌍 Free and Open-Source Translator (NLLB) for Indian Languages")

# Load NLLB model
@st.cache_resource
def load_model():
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Language code map
nllb_lang_codes = {
    'English': 'eng_Latn',
    'Hindi': 'hin_Deva',
    'Malayalam': 'mal_Mlym',
    'Tamil': 'tam_Taml',
    'Telugu': 'tel_Telu',
    'Bengali': 'ben_Beng',
    'Gujarati': 'guj_Gujr',
    'Kannada': 'kan_Knda',
    'Punjabi': 'pan_Guru',
    'Marathi': 'mar_Deva',
    'Odia': 'ory_Orya',
    'Assamese': 'asm_Beng',
    'Urdu': 'urd_Arab'
}

# Language selectors
src_lang = st.selectbox("Select source language", list(nllb_lang_codes.keys()))
tgt_lang = st.selectbox("Select target language", list(nllb_lang_codes.keys()))

# Input text
input_text = st.text_area("Enter text to translate", height=150)

# Translate button
if st.button("Translate"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    elif src_lang == tgt_lang:
        st.info("Source and target languages are the same.")
        st.write(input_text)
    else:
        try:
            src_code = nllb_lang_codes[src_lang]
            tgt_code = nllb_lang_codes[tgt_lang]

            tokenizer.src_lang = src_code
            inputs = tokenizer(input_text, return_tensors="pt", padding=True)
            inputs["forced_bos_token_id"] = tokenizer.lang_code_to_id[tgt_code]

            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=512)
                translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

            st.success("Translation:")
            st.text_area("Translated Output", translated_text, height=150)
        except Exception as e:
            st.error(f"Error: {e}")

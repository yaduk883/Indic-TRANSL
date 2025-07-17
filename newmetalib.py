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

import streamlit as st
from openai import OpenAI

# Cria cliente usando a chave do Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis do .env
load_dotenv()

# Cria cliente atual compatível com openai>=1.0.0
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Importa classes e funções do LangChain para interação com LLMs
from langchain_openai import ChatOpenAI  # Cliente OpenAI para chat
from langchain.prompts import PromptTemplate  # Templates de prompt
from langchain.schema import HumanMessage  # Representa a mensagem enviada pelo usuário
from langchain.callbacks.base import BaseCallbackHandler  # Base para callbacks durante streaming
import os
import json
from dotenv import load_dotenv  # Carrega variáveis de ambiente de um arquivo .env
import streamlit as st
# Carrega variáveis do arquivo .env (como a API key)
load_dotenv()

# Callback customizado para imprimir tokens gerados pelo modelo em tempo real
class PrintCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        """
        Função chamada a cada token gerado pelo LLM.
        Imprime o token imediatamente sem quebrar linha.
        """
        print(token, end='', flush=True)

def gerar_resumos(chunk, memoria=None):
    """
    Gera resumos de um pedaço de texto usando GPT-4 via LangChain.

    Args:
        chunk (str): Texto a ser resumido.
        memoria (list, opcional): Lista de mensagens anteriores para manter contexto.

    Returns:
        tuple: (resumos, memoria) 
            resumos: lista de dicionários com a chave 'resumo'
            memoria: lista atualizada de mensagens para contexto
    """
    if memoria is None:
        memoria = []  # Inicializa memória se não fornecida

    # Template de prompt para o modelo GPT
    prompt_template = """
    Gere um resumo do seguinte texto:
    {texto}

    Formato de saída JSON:
    [
        {{"resumo": "..."}}
    ]
    """
    # Cria um PromptTemplate substituindo a variável {texto} pelo chunk
    prompt = PromptTemplate(input_variables=["texto"], template=prompt_template)
    texto_prompt = prompt.format(texto=chunk)

    # Cria instância do modelo GPT-4 via LangChain
    llm = ChatOpenAI(
        openai_api_key = st.secrets["OPENAI_API_KEY"],  # Usa chave da variável de ambiente
        temperature=0.3,  # Temperatura baixa para respostas mais objetivas
        model_name="gpt-5",
        streaming=False,  # Não usar streaming de tokens neste caso
        callbacks=[PrintCallback()]  # Callback para imprimir tokens gerados
    )

    # Cria mensagem do usuário
    human_message = HumanMessage(content=texto_prompt)
    memoria.append(human_message)  # Adiciona à memória para contexto

    # Chama o modelo com a mensagem
    resposta_texto = llm.invoke([human_message])

    # Tenta converter a resposta em JSON
    try:
        resumos = json.loads(resposta_texto.content)
    except json.JSONDecodeError:
        # Se não for JSON válido, retorna a resposta como texto simples
        resumos = [{"resumo": resposta_texto.content}]

    return resumos, memoria

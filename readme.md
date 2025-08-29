# README.md

# 📚 RelembraQ é um Resumidor Inteligente de PDFs para Alunos Nunca Esquecerem do que Estudaram

Este projeto tem como objetivo **extrair e resumir automaticamente conteúdos de PDFs educacionais**, gerando **resumos inteligentes** e **mapas mentais** para facilitar o estudo dos alunos.

---

## ✨ Funcionalidades

1. **📄 Leitura de PDFs**

   * Percorre uma pasta contendo PDFs e extrai todo o texto contido neles.

2. **📝 Divisão em Chunks**

   * O texto é dividido em pedaços menores (chunks) para facilitar o processamento pelo modelo de IA.

3. **🤖 Geração de Resumos**

   * Cada chunk é processado por um modelo GPT-4 via LangChain, gerando resumos em formato JSON.
   * Mantém memória das interações para preservar contexto entre chunks.

4. **📊 Clusterização**

   * As sentenças resumidas são agrupadas em clusters usando embeddings da OpenAI e KMeans.
   * Número de clusters configurável pelo usuário.

5. **🧠 Mapas Mentais**

   * **Textual:** arquivo `.txt` para leitura rápida.
   * **Visual:** arquivo `.png` para visualização intuitiva dos tópicos.

6. **📈 Visualização 3D**

   * Gráfico 3D com redução de dimensionalidade via PCA.
   * Salva a figura em `outputs/clusters_3d.png`.

7. **💾 Exportação**

   * Resumos: `outputs/resumo_aula.json`
   * Mapas mentais: `outputs/mapa_mental.txt` e `outputs/mapa_mental.png`

---

## 📁 Estrutura do Projeto

```
resumidor/
│
├── materia/                  # PDFs de entrada
├── outputs/                  # Saídas geradas (resumos, mapas mentais, gráficos)
│
├── controllers/              # Funções de controle
│   ├── agent.py              # Geração de resumos com GPT
│   ├── ml_utils.py           # Clusterização e embeddings
│   ├── mindmap.py            # Criação de mapas mentais
│   └── visualizacao.py       # Visualização 3D dos clusters
│
├── models/
│   ├── chunking.py           # Divisão de texto em chunks
│   └── openai_client.py      # Cliente OpenAI
│
├── views/
│   └── output.py             # Função para salvar JSON
│
├── relembraq.py              # Script principal
├── requirements.txt          # Dependências do projeto
└── README.md
```

---

## 🚀 Como Usar

1. **Preparar PDFs**

   * Coloque todos os PDFs na pasta `materia/`.

2. **Configurar Variáveis de Ambiente**

   * Crie um arquivo `.env` com sua chave de API da OpenAI:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

4. **Executar o relembraq**

```bash
python relembraq.py
```

5. **Resultados**

* `outputs/resumo_aula.json` → Resumos gerados.
* `outputs/mapa_mental.txt` → Mapa mental textual.
* `outputs/mapa_mental.png` → Mapa mental visual.
* `outputs/clusters_3d.png` → Gráfico 3D de clusters.

---

## ⚙️ Personalização

* **Chunk Size:** tamanho do texto por chunk, padrão: `150`.
* **Número de Clusters:** quantidade de tópicos a gerar, padrão: `5`.

Ambos podem ser ajustados na função:

```python
resumidor_completo(chunk_size=150, n_clusters=5)
```

---

## 📝 Requisitos

* Python >= 3.10
* Dependências listadas em `requirements.txt`

---

## 📦 Dependências (requirements.txt)

```
python-dotenv
openai>=1.0.0
langchain
matplotlib
numpy
scikit-learn
PyMuPDF
graphviz
```

---

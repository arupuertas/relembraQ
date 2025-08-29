import os
import fitz  # PyMuPDF para manipulação de PDFs
import numpy as np
import matplotlib.pyplot as plt

# Importa funções do seu projeto
from models.chunking import chunk_text  # Função para dividir texto em pedaços
from controllers.agent import gerar_resumos  # Função que gera resumos com GPT
from controllers.ml_utils import cluster_sentencas  # Função para clusterizar sentenças
from controllers.mindmap import gerar_mapa_mental_textual_clusters, gerar_mapa_mental_visual_clusters  # Mapas mentais
from views.output import salvar_json  # Função para salvar arquivos JSON

# Pasta onde estão os PDFs de entrada
PASTA_PDFS = "materia"

# Garante que a pasta de saída exista
os.makedirs("outputs", exist_ok=True)


def extrair_texto_da_pasta(pasta):
    """
    Extrai todo o texto de todos os PDFs em uma pasta.
    Args:
        pasta (str): Caminho da pasta com PDFs.
    Returns:
        str: Texto completo extraído de todos os PDFs.
    """
    texto_total = ""
    # Lista apenas arquivos com extensão .pdf
    arquivos_pdf = [f for f in os.listdir(pasta) if f.endswith(".pdf")]
    for arquivo in arquivos_pdf:
        caminho = os.path.join(pasta, arquivo)
        doc = fitz.open(caminho)
        # Percorre todas as páginas do PDF
        for page in doc:
            texto_total += page.get_text()
    return texto_total


def plot_clusters_3d(embeddings, labels):
    """
    Plota um gráfico 3D dos embeddings de sentenças agrupados em clusters usando PCA.
    
    Args:
        embeddings (array): Embeddings das sentenças.
        labels (list): Labels de cluster correspondentes a cada embedding.
    """
    from mpl_toolkits.mplot3d import Axes3D
    from sklearn.decomposition import PCA

    # Reduz a dimensionalidade dos embeddings para 3D
    pca = PCA(n_components=3)
    coords = pca.fit_transform(embeddings)

    # Cria figura 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Define cores para cada cluster
    n_clusters = len(set(labels))
    colors = plt.cm.get_cmap('tab10', n_clusters)

    # Plota cada ponto com sua cor e label
    for i, (coord, label) in enumerate(zip(coords, labels)):
        ax.scatter(coord[0], coord[1], coord[2], color=colors(label), s=50)
        ax.text(coord[0], coord[1], coord[2], str(label+1), fontsize=9)

    # Configurações de título e eixos
    ax.set_title("Clusters de Resumos (PCA 3D)")
    ax.set_xlabel("PCA1")
    ax.set_ylabel("PCA2")
    ax.set_zlabel("PCA3")
    plt.tight_layout()

    # Salva a figura
    plt.savefig("outputs/clusters_3d.png")
    plt.show()
    print("[INFO] Gráfico 3D dos clusters salvo em 'outputs/clusters_3d.png'.")


def resumidor_completo(chunk_size=150, n_clusters=5):
    """
    Função principal que coordena todo o processo:
    - Extrai texto de PDFs
    - Divide em chunks
    - Gera resumos com GPT
    - Clusteriza resumos
    - Gera mapas mentais (textual e visual)
    - Plota gráfico 3D dos clusters
    
    Args:
        chunk_size (int): Quantidade de palavras por chunk.
        n_clusters (int): Número de clusters para agrupar os resumos.
        
    Returns:
        clusters (dict), labels (list), sentencas (list)
    """
    # Extrai texto dos PDFs
    texto = extrair_texto_da_pasta(PASTA_PDFS)
    print(f"[INFO] Texto extraído da pasta '{PASTA_PDFS}'.")

    # Divide o texto em chunks
    chunks = chunk_text(texto, chunk_size=chunk_size)
    print(f"[INFO] Texto total dividido em {len(chunks)} chunks.")

    todos_resumos = []  # Armazena todos os resumos
    memoria = []        # Memória para manter contexto entre chunks

    # Processa cada chunk gerando resumos
    for i, chunk in enumerate(chunks, start=1):
        print(f"[INFO] Processando chunk {i}/{len(chunks)}...")
        resumos, memoria = gerar_resumos(chunk, memoria)
        todos_resumos.extend(resumos)

    # Remove resumos duplicados
    resumos_unicos = list({r['resumo']: r for r in todos_resumos}.values())
    print(f"[INFO] Total de resumos únicos: {len(resumos_unicos)}")
    salvar_json(resumos_unicos, "outputs/resumo_aula.json")

    # Prepara sentenças para clusterização
    sentencas = [r['resumo'] for r in resumos_unicos]
    clusters, labels, embeddings = cluster_sentencas(
        sentencas, n_clusters=n_clusters, return_embeddings=True)
    print(f"[INFO] Resumos agrupados em {n_clusters} clusters.")

    # Gera mapa mental textual
    mapa_textual = gerar_mapa_mental_textual_clusters(clusters)
    with open("outputs/mapa_mental.txt", "w", encoding="utf-8") as f:
        f.write(mapa_textual)

    # Gera mapa mental visual
    gerar_mapa_mental_visual_clusters(clusters, "outputs/mapa_mental.png")
    print("[INFO] Mapas mentais gerados em 'outputs/'.")

    # Plota clusters em 3D
    plot_clusters_3d(embeddings, labels)

    return clusters, labels, sentencas

# Executa o resumidor se este script for o principal
if __name__ == "__main__":
    clusters, labels, sentencas = resumidor_completo(chunk_size=150, n_clusters=5)

    # Mostra os resumos agrupados por cluster no console
    for cluster_id, sentencas_cluster in clusters.items():
        print(f"\nTópico {cluster_id+1}:")
        for s in sentencas_cluster:
            print(f"- {s}")

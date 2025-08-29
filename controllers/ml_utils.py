from sklearn.cluster import KMeans  # Algoritmo de clusterização
from models.openai_client import client  # Cliente OpenAI para gerar embeddings
import numpy as np  # Biblioteca para manipulação de arrays

def cluster_sentencas(sentencas, n_clusters=5, return_embeddings=False):
    """
    Agrupa sentenças em clusters usando embeddings de linguagem e KMeans.
    Args:
        sentencas (list): Lista de sentenças a serem agrupadas.
        n_clusters (int): Número de clusters desejados. Padrão: 5.
        return_embeddings (bool): Se True, retorna também os embeddings gerados.
    Returns:
        clusters (dict): Dicionário com chave=ID do cluster e valor=lista de sentenças.
        labels (list): Lista com o label de cluster correspondente a cada sentença.
        embeddings (np.array, opcional): Array de embeddings, se return_embeddings=True.
    """
    embeddings = []
    # Gera embeddings para cada sentença usando o modelo da OpenAI
    for texto in sentencas:
        response = client.embeddings.create(model="text-embedding-3-small", input=texto)
        embeddings.append(response.data[0].embedding)
    
    embeddings = np.array(embeddings)  # Converte para array numpy para uso no KMeans

    # Cria e treina o modelo KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)  # Obtém o label de cluster para cada sentença

    # Cria dicionário de clusters
    clusters = {i: [] for i in range(n_clusters)}
    for sentenca, label in zip(sentencas, labels):
        clusters[label].append(sentenca)  # Adiciona a sentença ao cluster correspondente

    # Retorna resultados
    if return_embeddings:
        return clusters, labels, embeddings
    return clusters, labels

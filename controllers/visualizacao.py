# controllers/visualizacao.py
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

def plot_clusters_3d(embeddings, n_clusters=5, labels=None):
    """
    Plota um gráfico 3D dos embeddings agrupados por KMeans.
    
    embeddings: lista ou array de embeddings
    n_clusters: número de clusters
    labels: (opcional) labels originais para mostrar
    """
    # Reduz a dimensionalidade para 3D
    pca = PCA(n_components=3)
    X_3d = pca.fit_transform(embeddings)
    
    # KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_ids = kmeans.fit_predict(embeddings)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Cores para os clusters
    colors = plt.cm.tab10(cluster_ids / n_clusters)
    
    for i, (x, y, z) in enumerate(X_3d):
        ax.scatter(x, y, z, c=[colors[i]], s=60, edgecolor='k')
        ax.text(x, y, z, f"C{cluster_ids[i]}", fontsize=8)  # imprime cluster
    
    ax.set_title("Clusters KMeans (3D PCA)")
    ax.set_xlabel("PCA1")
    ax.set_ylabel("PCA2")
    ax.set_zlabel("PCA3")
    plt.show()
    
    return cluster_ids, X_3d

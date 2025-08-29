from graphviz import Digraph  # Importa a biblioteca Graphviz para criar diagramas

def gerar_mapa_mental_textual_clusters(clusters):
    """
    Gera um mapa mental em formato textual a partir de clusters de sentenças.
    Args:
        clusters (dict): Dicionário onde cada chave é um cluster e o valor é uma lista de sentenças.
    Returns:
        str: Representação textual do mapa mental, organizada por tópicos.
    """
    texto = ""
    # Itera sobre cada cluster
    for cluster_id, sentencas in clusters.items():
        texto += f"Tópico {cluster_id+1}:\n"  # Cabeçalho do tópico
        # Adiciona cada sentença do cluster como um item
        for s in sentencas:
            texto += f"- {s}\n"
        texto += "\n"  # Espaço entre tópicos
    return texto


def gerar_mapa_mental_visual_clusters(clusters, output_path):
    """
    Gera um mapa mental visual em formato de gráfico (PNG) a partir de clusters de sentenças.
    Args:
        clusters (dict): Dicionário onde cada chave é um cluster e o valor é uma lista de sentenças.
        output_path (str): Caminho para salvar o arquivo de saída (sem extensão, Graphviz adiciona .png).
    """
    dot = Digraph(comment="Mapa Mental")  # Cria um objeto Digraph

    # Itera sobre cada cluster
    for cluster_id, sentencas in clusters.items():
        parent_node = f"Cluster {cluster_id+1}"  # Nome do nó pai
        dot.node(parent_node, parent_node)       # Cria o nó pai

        # Itera sobre cada sentença no cluster e cria nós filhos
        for i, s in enumerate(sentencas):
            child_node = f"{cluster_id+1}_{i}"  # Nome único do nó filho
            # Trunca o texto do nó filho se for maior que 50 caracteres
            dot.node(child_node, s[:50] + "..." if len(s) > 50 else s)
            # Conecta o nó pai ao filho
            dot.edge(parent_node, child_node)

    # Renderiza e salva o gráfico em PNG, removendo arquivos temporários
    dot.render(output_path.replace(".png", ""), format="png", cleanup=True)

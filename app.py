import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF
from io import BytesIO
from streamlit_markmap import markmap  # mapa mental interativo
from relembraq import resumidor_completo

# Configuração inicial do Streamlit
st.set_page_config(page_title="RelembraQ", page_icon="🧠", layout="wide")

# Cabeçalho com logo e título lado a lado
col1, col2 = st.columns([1, 4])
with col1:
    st.image("img/logo.jpg", width=100)  # coloque o logo na mesma pasta do app ou ajuste o caminho
with col2:
    st.markdown("""
        <h3 style="
            color: #0f111a; 
            font-weight: 500; 
            line-height: 1.3; 
            margin-top: 0;
        ">
            🧠 RelembraQ — Seu Resumidor Inteligente.
        </h3>
        <p style="
            color: #555555; 
            font-size: 16px; 
            margin-top: 5px;
        ">
            O mais novo produto do grupoQ para agilizar seus estudos e organizar informações de forma inovadora.
        </p>
    """, unsafe_allow_html=True)
    
# Upload de arquivos
st.sidebar.header("📂 Upload dos PDFs")
uploaded_files = st.sidebar.file_uploader(
    "Selecione seus PDFs", type=["pdf"], accept_multiple_files=True
)

# Parâmetros ajustáveis
st.sidebar.header("⚙️ Configurações")
chunk_size = st.sidebar.slider("Tamanho do Chunk (palavras)", 50, 500, 150, 50)
n_clusters = st.sidebar.slider("Número de Clusters", 2, 10, 5, 1)

# Criar diretórios temporários
TEMP_PDF_DIR = tempfile.mkdtemp()
os.makedirs("outputs", exist_ok=True)

# Salvar PDFs enviados
pdf_paths = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        caminho = os.path.join(TEMP_PDF_DIR, uploaded_file.name)
        with open(caminho, "wb") as f:
            f.write(uploaded_file.getbuffer())
        pdf_paths.append(caminho)
    st.success(f"{len(uploaded_files)} arquivo(s) salvo(s) temporariamente para processamento.")

# Função para extrair texto apenas dos PDFs selecionados
def extrair_texto_selecionados(paths):
    texto_total = ""
    for caminho in paths:
        doc = fitz.open(caminho)
        for page in doc:
            texto_total += page.get_text()
    return texto_total

# Botão para rodar o resumidor
if st.button("🚀 Rodar Resumidor"):
    if not uploaded_files:
        st.warning("⚠️ Por favor, envie pelo menos um PDF antes de rodar.")
    else:
        st.info("⏳ Processando PDFs, isso pode levar alguns minutos...")

        # Extrai texto dos PDFs selecionados
        texto = extrair_texto_selecionados(pdf_paths)

        # Divide em chunks
        from models.chunking import chunk_text
        chunks = chunk_text(texto, chunk_size=chunk_size)
        st.write(f"Total de chunks a processar: {len(chunks)}")

        todos_resumos = []
        memoria = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        # Processa cada chunk com barra de progresso
        from controllers.agent import gerar_resumos
        for i, chunk in enumerate(chunks, start=1):
            status_text.text(f"Processando chunk {i}/{len(chunks)}...")
            resumos, memoria = gerar_resumos(chunk, memoria)
            todos_resumos.extend(resumos)
            progress_bar.progress(i / len(chunks))

        status_text.text("✅ Processamento concluído!")

        # Remove resumos duplicados
        resumos_unicos = list({r['resumo']: r for r in todos_resumos}.values())

        # Salva JSON
        from views.output import salvar_json
        salvar_json(resumos_unicos, "outputs/resumo_aula.json")

        # Clusterização
        from controllers.ml_utils import cluster_sentencas
        sentencas = [r['resumo'] for r in resumos_unicos]
        clusters, labels, embeddings = cluster_sentencas(sentencas, n_clusters=n_clusters, return_embeddings=True)

        st.success("✅ Resumos e Clusters gerados com sucesso!")

        # Mostrar clusters no app
        for cluster_id, sentencas_cluster in clusters.items():
            with st.expander(f"Tópico {cluster_id+1}"):
                for s in sentencas_cluster:
                    st.write(f"- {s}")

        # Mostrar mapa mental interativo
        from controllers.mindmap import gerar_mapa_mental_textual_clusters
        mapa_textual = gerar_mapa_mental_textual_clusters(clusters)
        st.subheader("🧠 Mapa Mental Interativo")
        markmap(mapa_textual)

        # Mostrar arquivos gerados
        st.subheader("📄 Arquivos Gerados")
        st.write("- `outputs/resumo_aula.json`")

        # Mostrar gráfico 3D
        st.subheader("📊 Gráfico 3D de Clusters")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from sklearn.decomposition import PCA

        pca = PCA(n_components=3)
        coords = pca.fit_transform(embeddings)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        n_clusters_ = len(set(labels))
        cmap = plt.colormaps['tab10']
        colors = [cmap(i) for i in range(n_clusters_)]  # lista de cores
        for i, (coord, label) in enumerate(zip(coords, labels)):
            ax.scatter(coord[0], coord[1], coord[2], color=colors[label], s=50)
            ax.text(coord[0], coord[1], coord[2], str(label+1), fontsize=9)
        ax.set_title("Clusters de Resumos (PCA 3D)")
        ax.set_xlabel("PCA1")
        ax.set_ylabel("PCA2")
        ax.set_zlabel("PCA3")
        st.pyplot(fig)

        st.info("📌 PCA 3D mostra como os resumos estão distribuídos nos clusters. Cada ponto é um resumo, cores diferentes representam clusters distintos.")

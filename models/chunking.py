def chunk_text(text, chunk_size=200):
    """
    Divide um texto longo em pedaços menores (chunks) para facilitar processamento.
    Args:
        text (str): Texto completo a ser dividido.
        chunk_size (int): Número máximo de palavras por chunk. Padrão é 200.
    Returns:
        list: Lista de strings, cada uma representando um chunk do texto.
    """
    # Divide o texto em uma lista de palavras
    words = text.split()
    # Lista que vai armazenar os chunks
    chunks = []
    # Percorre a lista de palavras em passos de tamanho chunk_size
    for i in range(0, len(words), chunk_size):
        # Junta as palavras do intervalo atual em uma única string e adiciona à lista de chunks
        chunks.append(" ".join(words[i:i+chunk_size]))

    # Retorna a lista de chunks
    return chunks

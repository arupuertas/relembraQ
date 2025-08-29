import json  # Importa o módulo JSON para manipulação de arquivos JSON

def salvar_json(dados, caminho):
    """
    Salva dados em um arquivo no formato JSON.

    Args:
        dados (any): Estrutura de dados Python (lista, dicionário, etc.) que será salva.
        caminho (str): Caminho completo do arquivo onde os dados serão salvos.

    Funcionalidade:
        - Abre o arquivo no modo de escrita ("w") com codificação UTF-8.
        - Usa json.dump para escrever os dados no arquivo em formato JSON.
        - ensure_ascii=False permite que caracteres especiais (como acentos) sejam preservados.
        - indent=4 formata o JSON com identação para facilitar a leitura.
    """
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

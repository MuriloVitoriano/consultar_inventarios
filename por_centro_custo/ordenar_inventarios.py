import os
import json

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

# 1. Caminho para a pasta que contém os arquivos JSON
PASTA_JSON = 'por_centro_custo'

# 2. Chave para ordenar os inventários DENTRO de cada arquivo JSON
# Você pode mudar para: 'Inventarios', 'Equipamentos', 'Area', etc.
CHAVE_ORDENACAO = 'Equipamentos' 

# ======================================================================
# FUNÇÃO PRINCIPAL
# ======================================================================

def ordenar_arquivos_json_por_chave(pasta, chave):
    """
    Lista todos os arquivos .json na pasta especificada, ordena o conteúdo
    (que deve ser uma lista de dicionários) pela chave fornecida e salva.
    """
    
    # 1. Lista todos os arquivos na pasta
    try:
        arquivos = [f for f in os.listdir(pasta) if f.endswith('.json')]
    except FileNotFoundError:
        print(f"ERRO: A pasta '{pasta}' não foi encontrada. Verifique o caminho.")
        return

    if not arquivos:
        print(f"Nenhum arquivo .json encontrado na pasta '{pasta}'.")
        return

    print(f"Iniciando ordenação em {len(arquivos)} arquivos pela chave: '{chave}'...")
    
    # 2. Itera sobre cada arquivo JSON
    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(pasta, nome_arquivo)
        
        try:
            # Lendo o arquivo
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Verifica se o conteúdo é uma lista (esperado para o seu formato)
            if not isinstance(dados, list):
                print(f"AVISO: O arquivo {nome_arquivo} não é uma lista e será ignorado.")
                continue

            # 3. Ordena a lista de dicionários
            # Usamos uma função lambda para ordenar pelo valor da chave
            dados_ordenados = sorted(
                dados, 
                key=lambda item: item.get(chave, ''), # Usa uma string vazia se a chave não existir
                # Caso a chave seja numérica (como Centro de Custo), você pode precisar de:
                # key=lambda item: str(item.get(chave, '')).zfill(10) 
            )

            # 4. Sobrescreve o arquivo original com os dados ordenados
            # O indent=2 garante que o arquivo seja reescrito formatado e legível
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                json.dump(dados_ordenados, f, indent=2, ensure_ascii=False)
            
            print(f"  -> Arquivo {nome_arquivo} ordenado com sucesso.")

        except json.JSONDecodeError:
            print(f"ERRO: Falha ao decodificar JSON no arquivo {nome_arquivo}. Verifique a sintaxe do JSON.")
        except Exception as e:
            print(f"ERRO inesperado ao processar {nome_arquivo}: {e}")

    print("\nProcesso de ordenação concluído.")

# ======================================================================
# EXECUÇÃO
# ======================================================================

if __name__ == "__main__":
    ordenar_arquivos_json_por_chave(PASTA_JSON, CHAVE_ORDENACAO)
import os
import json

def carregar_conhecimento(diretorio_txt="arquivo_txt", arquivo_saida="database/knowledge.json"):
    conhecimento = {}

    for nome_arquivo in os.listdir(diretorio_txt):
        if nome_arquivo.endswith(".txt"):
            caminho = os.path.join(diretorio_txt, nome_arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                categoria = nome_arquivo.replace(".txt", "")
                conhecimento[categoria] = f.read()

    with open(arquivo_saida, "w", encoding="utf-8") as f_out:
        json.dump(conhecimento, f_out, ensure_ascii=False, indent=2)

    print("✅ Conhecimento atualizado.")


if __name__ == "__main__":
    carregar_conhecimento()
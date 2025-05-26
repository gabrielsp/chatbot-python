import json
import os
import unicodedata

class RespostaEmpresa:
    def __init__(self):
        self.dados = self.carregar_base_conhecimento()

    def carregar_base_conhecimento(self):
        try:
            with open('database/knowledge.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print("Erro ao carregar base de conhecimento:", e)
            return []

    def normalizar_texto(self, texto):
        texto = texto.lower().strip()
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto

    def executar(self, numero, texto_usuario, contexto):
        texto_usuario = self.normalizar_texto(texto_usuario)

        for item in self.dados:
            pergunta = self.normalizar_texto(item.get("pergunta", ""))
            if pergunta in texto_usuario or texto_usuario in pergunta:
                return item.get("resposta")

        return None

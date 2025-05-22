import json
from .base import EstrategiaResposta

class RespostaEmpresa(EstrategiaResposta):
    def __init__(self, arquivo_conhecimento="database/knowledge.json"):
        with open(arquivo_conhecimento, "r", encoding="utf-8") as f:
            self.conhecimento = json.load(f)

    def executar(self, numero, mensagem, contexto):
        return self.responder(mensagem)

    def responder(self, pergunta):
        pergunta = pergunta.lower()
        for categoria, conteudo in self.conhecimento.items():
            if any(palavra in pergunta for palavra in categoria.lower().split()):
                return f"🔎 Informações sobre '{categoria}':\n{conteudo}"
        return "❓ Desculpe, não encontrei essa informação nos dados da empresa."

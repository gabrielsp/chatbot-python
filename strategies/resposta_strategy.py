import json
import unicodedata
import os
import requests
from .base import EstrategiaResposta

class RespostaEmpresa:
    def __init__(self):
        self.dados = self.carregar_base_conhecimento()

    def carregar_base_conhecimento(self):
        try:
            with open('database/knowledge.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print("Erro ao carregar base de conhecimento:", e)
            return {}

    def normalizar_texto(self, texto):
        texto = texto.lower().strip()
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto

    def buscar_trechos_relevantes(self, pergunta):
        trechos_relevantes = []
        for chave, conteudo in self.dados.items():
            if any(palavra in conteudo.lower() for palavra in pergunta.lower().split()):
                trechos_relevantes.append(conteudo)
        return "\n\n".join(trechos_relevantes[:3])  # Limita a 3 blocos

    def gerar_resposta_ollama(self, pergunta, contexto_txt):
        prompt = (
            "Você é um assistente virtual treinado para responder perguntas com base exclusivamente nas informações abaixo.\n\n"
            f"{contexto_txt}\n\n"
            f"Pergunta: {pergunta}\n"
            "Resposta:"
        )
        try:
            resposta = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",  # ou "mistral", "phi", etc.
                    "prompt": prompt,
                    "stream": False
                }
            )
            if resposta.status_code == 200:
                return resposta.json()['response'].strip()
            else:
                print("Erro do Ollama:", resposta.text)
                return None
        except Exception as e:
            print("Erro na comunicação com Ollama:", e)
            return None

    def executar(self, numero, texto_usuario, contexto):
        texto_usuario = texto_usuario.strip()

        trechos = self.buscar_trechos_relevantes(texto_usuario)
        if not trechos:
            return "Desculpe, não encontrei informações suficientes para responder sua pergunta."

        resposta = self.gerar_resposta_ollama(texto_usuario, trechos)
        return resposta or "Desculpe, não consegui gerar uma resposta no momento."

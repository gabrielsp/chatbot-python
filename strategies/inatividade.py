import time
from datetime import datetime, timedelta
from webhook import enviar_mensagem

TEMPO_LIMITE_MINUTOS = 5

class MonitorInatividade:
    def __init__(self, interacoes):
        self.ultimas_interacoes = interacoes

    def verificar(self, historico):
        agora = datetime.now()

        for numero in historico.keys():
            ultima = self.ultimas_interacoes.get(numero, agora)
            if agora - ultima > timedelta(minutes=TEMPO_LIMITE_MINUTOS):
                enviar_mensagem(numero, "Percebi que você está ausente. Se precisar de algo, estarei por aqui! 😊")
                self.ultimas_interacoes[numero] = agora

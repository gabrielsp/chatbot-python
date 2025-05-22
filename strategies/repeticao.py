from datetime import datetime, timedelta

class EvitarRepeticao:
    TEMPO_REPETICAO_MINUTOS = 1

    def __init__(self):
        self.ultimas_mensagens = {}

    def executar(self, numero, mensagem, contexto):
        agora = datetime.now()
        historico = contexto.get("historico_usuarios", {})

        if numero not in historico:
            historico[numero] = []

        if numero in self.ultimas_mensagens:
            ultima_mensagem, ultimo_tempo = self.ultimas_mensagens[numero]
            if mensagem == ultima_mensagem and agora - ultimo_tempo < timedelta(minutes=self.TEMPO_REPETICAO_MINUTOS):
                return False

        historico[numero].append({"mensagem": mensagem, "hora": agora.strftime('%H:%M:%S')})
        contexto["ultimas_interacoes"][numero] = agora
        self.ultimas_mensagens[numero] = (mensagem, agora)
        return True

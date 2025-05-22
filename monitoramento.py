from strategies.inatividade import MonitorInatividade
from webhook import historico_usuarios, ultimas_interacoes
import time

monitor = MonitorInatividade(ultimas_interacoes)

if __name__ == '__main__':
    while True:
        monitor.verificar(historico_usuarios)
        time.sleep(60)

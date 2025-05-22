from abc import ABC, abstractmethod

class EstrategiaResposta(ABC):
    @abstractmethod
    def executar(self, numero, mensagem, contexto):
        pass

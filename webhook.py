from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime
import os, requests, json
from strategies.repeticao import EvitarRepeticao
from strategies.resposta_strategy import RespostaEmpresa

gerador_resposta = RespostaEmpresa()

app = Flask(__name__)
load_dotenv()

historico_usuarios = {}
ultimas_interacoes = {}

# Estratégias
filtro_repeticao = EvitarRepeticao()

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

@app.route('/webhook', methods=['GET'])
def verificar():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Token inválido', 403

@app.route('/webhook', methods=['POST'])
def receber_mensagem():
    data = request.get_json()
    print(json.dumps(data, indent=2))

    try:
        changes = data['entry'][0]['changes'][0]['value']
        if 'messages' in changes:
            mensagem = changes['messages'][0]
            texto = mensagem['text']['body']
            numero = mensagem['from']

            contexto = {
                'historico_usuarios': historico_usuarios,
                'ultimas_interacoes': ultimas_interacoes
            }

            if not filtro_repeticao.executar(numero, texto, contexto):
                return 'OK', 200

            resposta = gerador_resposta.executar(numero, texto, contexto)
            enviar_mensagem(numero, resposta)
    except Exception as e:
        print("Erro:", e)

    return 'OK', 200

def enviar_mensagem(destinatario, texto):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(port=5000)

from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os, requests, json

from strategies.repeticao import EvitarRepeticao
from strategies.resposta_strategy import RespostaEmpresa
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

load_dotenv()

# Estratégias
gerador_resposta = RespostaEmpresa()
filtro_repeticao = EvitarRepeticao()

# Tokens e variáveis de ambiente
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

# Dados em memória
historico_usuarios = {}
ultimas_interacoes = {}

# ---------------------- Funções auxiliares ------------------------

def gerar_menu_informacoes():
    try:
        with open('database/knowledge.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)

        topicos = set()
        for item in dados:
            pergunta = item.get("pergunta", "").strip().capitalize()
            if pergunta:
                topicos.add(pergunta)

        menu = "\n".join([f"🔹 {topico}" for topico in sorted(topicos)])
        return menu
    except Exception as e:
        print("Erro ao gerar menu:", e)
        return "⚠️ Não foi possível carregar os dados no momento."

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

def salvar_conversa(numero, texto, tipo='usuario'):
    log_path = 'logs/conversas.json'
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        else:
            dados = {}

        if numero not in dados:
            dados[numero] = []

        dados[numero].append({
            'tipo': tipo,
            'mensagem': texto,
            'timestamp': datetime.now().isoformat()
        })

        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Erro ao salvar conversa:", e)

def precisa_mensagem_boas_vindas(numero):
    ultima = ultimas_interacoes.get(numero)
    agora = datetime.now()
    return not ultima or (agora - ultima) > timedelta(hours=24)

def precisa_finalizar_conversa(numero):
    ultima = ultimas_interacoes.get(numero)
    agora = datetime.now()
    return ultima and (agora + timedelta(minutes=30)) < agora

# ------------------------ Rotas Flask ----------------------------

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
            agora = datetime.now()

            # Salva mensagem do usuário
            salvar_conversa(numero, texto, tipo='usuario')

            # Atualiza histórico e tempo da última interação
            historico_usuarios.setdefault(numero, [])
            historico_usuarios[numero].append({'mensagem': texto, 'timestamp': agora.isoformat()})
            ultimas_interacoes[numero] = agora

            contexto = {
                'historico_usuarios': historico_usuarios,
                'ultimas_interacoes': ultimas_interacoes
            }

            # Boas-vindas se primeira do dia
            if precisa_mensagem_boas_vindas(numero):
                menu = gerar_menu_informacoes()
                msg = (
                    "👋 Olá! Bem-vindo ao atendimento automático da *[Nome da Sua Empresa]*.\n\n"
                    "Estou aqui para te ajudar com informações da empresa. Veja alguns tópicos disponíveis:\n\n"
                    f"{menu}\n\n"
                    "Digite uma palavra-chave ou pergunta. 😉"
                )
                enviar_mensagem(numero, msg)
                salvar_conversa(numero, msg, tipo='bot')
                return 'OK', 200

            # Verifica repetição
            if not filtro_repeticao.executar(numero, texto, contexto):
                return 'OK', 200

            # Gera resposta
            resposta = gerador_resposta.executar(numero, texto, contexto)
            if not resposta:
                resposta = "Desculpe, não encontrei essa informação nos dados da empresa."

            enviar_mensagem(numero, resposta)
            salvar_conversa(numero, resposta, tipo='bot')

    except Exception as e:
        print("Erro no processamento:", e)

    return 'OK', 200

# ------------------ Rotina de encerramento (opcional com scheduler) ------------------

# Aqui você poderia usar um scheduler (como APScheduler ou cron) para verificar inatividade
# e enviar mensagens de encerramento. Exemplo:

def encerrar_conversas_inativas():
    agora = datetime.now()
    inativos = []

    for numero, ultima in list(ultimas_interacoes.items()):
        if (agora - ultima) > timedelta(minutes=30):
            mensagem = (
                "✅ Encerramos sua sessão de atendimento por inatividade.\n"
                "Caso tenha mais dúvidas, é só enviar uma nova mensagem. 😊"
            )
            enviar_mensagem(numero, mensagem)
            salvar_conversa(numero, mensagem, tipo='bot')
            del ultimas_interacoes[numero]

# ------------------- Execução com agendador -----------------------

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)

    # Inicia o agendador
    scheduler = BackgroundScheduler()
    scheduler.add_job(encerrar_conversas_inativas, 'interval', minutes=5)
    scheduler.start()

    try:
        app.run(port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
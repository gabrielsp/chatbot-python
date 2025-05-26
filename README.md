# Chatbot WhatsApp com Ollama

Este é um chatbot para WhatsApp que utiliza a API do WhatsApp Business e Ollama como motor de IA para processamento de linguagem natural.

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Ollama** - Motor de IA local para processamento de linguagem natural
- **Flask** - Framework web para gerenciamento de webhooks
- **Ngrok** - Tunelamento para expor o servidor local à internet
- **WhatsApp Business API** - Integração com WhatsApp

## 📦 Dependências Principais

- Flask==3.1.0
- ollama==0.4.8
- python-dotenv==1.1.0
- requests==2.32.3
- pydantic==2.11.4

## 🛠️ Configuração do Ambiente

1. Clone o repositório
```bash
git clone [URL_DO_REPOSITÓRIO]
cd chatbot-python
```

2. Crie e ative um ambiente virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
WHATSAPP_TOKEN=seu_token_aqui
VERIFY_TOKEN=seu_verify_token_aqui
```

5. Instale e configure o Ollama
- Siga as instruções de instalação em [ollama.ai](https://ollama.ai)
- Certifique-se que o serviço do Ollama está rodando localmente

6. Inicie o servidor Flask
```bash
python webhook.py
```

7. Configure o Ngrok
```bash
ngrok http 5000
```

## 📱 Integração com WhatsApp

1. Configure o webhook no painel do WhatsApp Business API
2. Use a URL do Ngrok como webhook URL
3. Configure o token de verificação definido no arquivo .env

## 📁 Estrutura do Projeto

```
chatbot-python/
├── .venv/               # Ambiente virtual Python
├── strategies/          # Estratégias de processamento
├── logs/               # Logs do sistema
├── database/           # Arquivos de banco de dados
├── arquivo_txt/        # Arquivos de texto
├── webhook.py          # Servidor Flask e lógica principal
├── send_whatsapp.py    # Funções de envio de mensagens
├── monitoramento.py    # Script de monitoramento
└── requirements.txt    # Dependências do projeto
```

## 🔄 Fluxo de Funcionamento

1. O servidor Flask recebe as mensagens do WhatsApp via webhook
2. As mensagens são processadas pelo Ollama
3. As respostas são enviadas de volta ao usuário via API do WhatsApp

## 📝 Notas Adicionais

- O sistema utiliza logs para monitoramento e debugging
- As estratégias de processamento podem ser personalizadas na pasta `strategies/`
- O monitoramento do sistema pode ser feito através do `monitoramento.py`

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

Este é um chatbot desenvolvido em Python com Flask que responde automaticamente mensagens recebidas via API do WhatsApp Business.

## 📂 Estrutura


import requests

# Substitua com seu token e número
token = 'EAAJln7rUkZAMBO2kmwI9hrZCxQ17gaBepUvPBj3pMQLGBRkJjQpL0CrW4ZBEbnRt0H6cSN8lzZCWm9N3bjNeGi8gsZBSh8qA2pNEkmVC0ZBhBTt5CZAboNGHoZCiqiiVjnWKBDffYaBJ1lbZBkT85QYSPRm754qLNavu1SKNgVQPLXX4anr2ridH17vYhZAMoHZCVLIzyyiZBnvuX064FkdT1mmprtKJpJ3k'
phone_number_id = '631136103418692'
numero_destino = '5521997251361'  # Ex: 5511999999999

url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

mensagem = {
    "messaging_product": "whatsapp",
    "to": numero_destino,
    "type": "text",
    "text": {
        "body": "Olá! Esta é uma mensagem enviada via WhatsApp Cloud API usando Python!"
    }
}

resposta = requests.post(url, headers=headers, json=mensagem)

print("Status:", resposta.status_code)
print("Resposta:", resposta.json())

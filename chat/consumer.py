import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    # Metoda volaná při připojení nového klienta přes WebSocket
    async def connect(self):
        # Přidání klienta do skupiny "chat" pro broadcast zpráv
        await self.channel_layer.group_add("chat", self.channel_name)
        # Potvrzení připojení klientovi
        await self.accept()

    # Metoda volaná při odpojení klienta
    async def disconnect(self, close_code):
        # Odebrání klienta ze skupiny "chat"
        await self.channel_layer.group_discard("chat", self.channel_name)

    # Zpracování příchozí zprávy od klienta přes WebSocket
    async def receive(self, text_data):
        # Převod JSON dat na Python slovník
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Získání uživatelského jména přihlášeného uživatele
        username = self.scope["user"].username

        # Odeslání zprávy všem klientům ve skupině "chat"
        await self.channel_layer.group_send(
            "chat",
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Metoda pro zpracování zprávy přijaté ze skupiny
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Odeslání zprávy konkrétnímu klientovi
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

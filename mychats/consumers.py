import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from django.contrib.auth.models import User
from chat.models import Message, ThreadChat

class ChatConsumer(WebsocketConsumer):
    
    def fetch_messages(self, data):
        messages = Message.objects.all().order_by('-date')[:10]
        content = {
            'messages':self.messages_to_json(messages)
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        
        return {
            'user':message.user.id,
            'sender':message.sender.id,
            'recipent':message.recipent.id,
            'body':message.body,
            'thread':message.thread.id,
            'date':str(message.date)
        }

    def new_message(self, data):
        
        user = data['from']
        sender = User.objects.filter(username=user)[0]
        message = Message.objects.create(user_id=sender.id, sender_id=sender.id, recipent_id=4, body=data['message'], thread_id=1)
        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }

        return self.send_chat_message(content)
        
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
    
        message = event['message']
         # Send message to WebSocket
        self.send(text_data=json.dumps({
            'command':'fetch_message',
            'message': message
        }))

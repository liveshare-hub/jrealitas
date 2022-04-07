import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from kepesertaan.models import Profile, Perusahaan
from chat.models import Message
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string

class NewUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected!")
        await self.channel_layer.group_add("users", self.channel_name)
        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, True)
            
            await self.send_status()

        await self.accept()

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard("users", self.channel_name)

        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, False)
            await self.send_status()

    
    async def send_status(self):
        users = await self.get_all_users()
        chats = await self.get_messages_status(users)
        chat_count = await self.get_messages_count(users)
        html_users =  await self.render_html(chats)
        await self.channel_layer.group_send (
        'users',
            {
            "type": "user_update",
            "event": "Change Status",
            # "html_users": html_users,
            "chat_users": chats,
            "chat_count": chat_count
            }
        )

    async def receive(self, text_data):
        text_data_json = await json.loads(text_data)
        
        print("connnn")
        print(text_data_json)


    async def user_update(self, event):
        
        await self.send(text_data=json.dumps(event))
        print ('user_update', event)

    @database_sync_to_async
    def update_user_status(self, user, status):
        
        pejabat = Profile.objects.select_related('username').all()
        if pejabat.filter(username__id=user.pk).exists():
            res = pejabat.filter(username__id=user.pk).update(status=status)
        else:
            res = Perusahaan.objects.filter(username__id=user.pk).update(status=status)
        return res

    @database_sync_to_async
    def get_all_users(self):
        user = self.scope['user']
        
        pejabat = Profile.objects.select_related('username').all()
        if pejabat.filter(username__username=user).exists():
            users = Perusahaan.objects.all()
        else:
            users = pejabat.exclude(username__username=user)
        return users

    @database_sync_to_async
    def get_messages_status(self, users):
        # user = self.scope['user']
        pesan = Message.objects.select_related('sender').all()
        for user in users:
            chat = pesan.filter(is_read=False).annotate(total=Count('is_read')).exclude(sender__username=user).values('is_read','sender__username','total')
            # chat = pesan.filter(is_read=False).exclude(sender__username=user)
        list_chat = json.dumps(list(chat), cls=DjangoJSONEncoder)
        # print(chat)
        return list_chat

    @database_sync_to_async
    def get_messages_count(self, users):
        # user = self.scope['user']
        pesan = Message.objects.select_related('sender').all()
        for user in users:
            total = pesan.filter(is_read=False).exclude(sender__username=user).count()
        # list_chat = list(chat)
        return total
        

    @sync_to_async
    def render_html(self, chats):
        return render_to_string("chat/users.html", {'chats': chats})
import asyncio 
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from kepesertaan.models import Profile, Perusahaan
from django.contrib.auth.models import User
from django.template.loader import render_to_string

class NewUserConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("users", self.channel_name)
        
        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status (user, True)
            await self.send_status()	

    async def disconnect (self, code):
        await self.channel_layer.group_discard("users", self.channel_name)

        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, False)
            await self.send_status()

    async def send_status(self):
        users = await self.get_all_users()
        html_users =  await self.render_html(users)
        await self.channel_layer.group_send (
        'users',
        {
            "type": "user_update",
            "event": "Change Status",
            "html_users": html_users
            }
        )

    async def user_update(self, event):
        await self.send_json(event)
        print ('user_update', event)

    @database_sync_to_async
    def update_user_status(self, user, status):
        print(user.pk)
        return Profile.objects.filter(user__username_id=user.pk).update(status=status)

    @sync_to_async
    def get_all_users(self):
        user = self.scope['user']
        print(user)
        return Profile.objects.all()

    @sync_to_async
    def render_html(self, users):
        return render_to_string("chat/users.html", {'users': users})
from django.contrib import admin

from .models import Message, ThreadChat, Thread, ChatMessage

admin.site.register(Message)
admin.site.register(ThreadChat)
admin.site.register(Thread)
admin.site.register(ChatMessage)
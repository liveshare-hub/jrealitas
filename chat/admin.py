from django.contrib import admin

from .models import Message, ThreadChat

admin.site.register(Message)
admin.site.register(ThreadChat)
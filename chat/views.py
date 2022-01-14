from django.contrib.auth.models import User
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.http import HttpResponse
from django.template import loader

from .chatencoder import ChatEncoder
from kepesertaan.models import Perusahaan, Profile


@login_required
def inbox(request):
    # user_obj = User.objects.get(username=username)
    users = Profile.objects.exclude(username__username=request.user)
    hrd = Perusahaan.objects.select_related('username','pembina').filter(pembina__username__username=request.user)

    
    return render(request, 'chat/direct.html',{'users':users,'hrds':hrd})
   
def chatbox(request, username):
    pass

def load_chat(request):
    user = request.user
    to_user = request.POST.get('to_user')
    messages = Message.objects.filter(sender__username=user, recipent__username=to_user)
    
    if messages.exists():
        list_messages = serializers.serialize('json',messages)
        print(list_messages)
        # list_messages = ChatEncoder().encode(messages)
    #     list_messages = messages.values()[0]
    #     print(list_messages)
        return JsonResponse({'data':list_messages})
    else:
        return JsonResponse({})
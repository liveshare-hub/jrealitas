from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.http import HttpResponse
from django.template import loader

from kepesertaan.models import Profile

@login_required
def inbox(request):
    # user_obj = User.objects.get(username=username)
    users = Profile.objects.exclude(username__username=request.user)
    return render(request, 'chat/direct.html',{'users':users})
   
def chatbox(request, username):
    pass

def load_chat(request):
    user = request.user
    to_user = request.POST.get('to_user')
    print(to_user)
    messages = Message.objects.filter(sender__username=user, recipent__username=to_user)
    print(messages)
    if messages.exists():
        list_messages = list(messages)
        return JsonResponse({'data':list_messages})
    else:
        return JsonResponse({'data':'gak ada pesan'})
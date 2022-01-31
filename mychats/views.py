import json
from django.shortcuts import render
from django.utils.safestring import mark_safe
# Create your views here.

def index(request):
    return render(request, 'mychats/index.html')

def room(request, room_name):

    context = {
        'room_name':room_name,
        'username':request.user.username
    }
    return render(request, 'mychats/room.html',context)
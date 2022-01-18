from genericpath import exists
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Message, ThreadChat
from django.http import HttpResponse
from django.template import loader

from .chatencoder import ChatEncoder
from kepesertaan.models import Perusahaan, Profile


@login_required
def inbox(request):
    # user_obj = User.objects.get(username=u
    users_jab = Profile.objects.select_related('username').filter(username__username=request.user)
    if users_jab.exists() :
        users = Profile.objects.exclude(username__username=request.user)
        hrd = Perusahaan.objects.all()
    else:
        users = Profile.objects.exclude(jabatan__kode_jabatan='70')
        # hrd = Perusahaan.objects.select_related('username','pembina').filter(pembina__username__username=request.user)
        hrd = Perusahaan.objects.none()

    context = {
        'users_jab':users_jab,
        'users':users,
        'hrds':hrd
    }
    
    return render(request, 'chat/direct.html',context)
   
def chatbox(request, username):
    pass

@csrf_exempt
def load_chat(request):
    user = request.user.pk
    to_user = request.POST.get('to_user')
    to_user_pk = User.objects.get(username=to_user)
    threads = ThreadChat.objects.all().filter(Q(user_id=user)|Q(to_user_id=user),Q(user_id=to_user_pk.pk)|Q(to_user_id=to_user_pk.pk))

    messages = Message.objects.all().filter(thread_id=threads[0].id)
    
    if messages.exists():
        list_messages = serializers.serialize('json',messages)
        
        return JsonResponse({'data':list_messages})
    else:
        return JsonResponse({})

@csrf_exempt
def create_chat(request):
    from_user = request.user.pk

    to_user = request.POST.get('to_user')
    to_user_pk = User.objects.get(username=to_user)
    cek_id = ThreadChat.objects.select_related('user','to_user').filter(user=from_user, to_user=to_user_pk.id)
    threads = serializers.serialize('json', cek_id)
    if cek_id.exists():
        return JsonResponse({'data':threads})
    else:
        threads = ThreadChat.objects.create(user_id=from_user, to_user_id=to_user_pk.id)

        return JsonResponse({'success':'Save!'})

@csrf_exempt
def save_chat(request):
    user = request.user.pk
    to_user = request.POST.get('to_user')
    body = request.POST.get('pesan')
    # to_user_pk = User.objects.get(username=to_user)
    cek_id = ThreadChat.objects.filter(Q(user_id=user)|Q(to_user_id=user),Q(user_id=int(to_user)|Q(to_user_id=int(to_user))))
    if cek_id.exists():  
        pesan = Message.objects.create(thread_id=cek_id.id, user_id=user, sender_id=user, recipent_id=int(to_user), body=body)
    
    return JsonResponse({'success':'message save'})

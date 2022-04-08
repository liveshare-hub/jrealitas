from django.db.models import Q
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Message, ThreadChat

from kepesertaan.models import Perusahaan, Profile


#testing channels
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponseForbidden
from django.views.generic.edit import FormMixin

from .forms import ComposeForm
from .models import Thread, ChatMessage


@login_required
def index(request):
    users_jab = Profile.objects.select_related('username').filter(username__username=request.user)
    
    if users_jab.exists() :
        users = Profile.objects.exclude(username__username=request.user)
        hrd = Perusahaan.objects.all()
    else:
        users = Profile.objects.exclude(jabatan__kode_jabatan='70')
        
        hrd = Perusahaan.objects.none()

    context = {
        'users_jab':users_jab,
        'users':users,
        'hrds':hrd
    }
    return render(request, 'chat/messages.html',context)

@login_required
def inbox(request):
    pesan = Message.objects.filter(is_read=False).all()
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
        'hrds':hrd,
        'chats':pesan,
    }
    
    return render(request, 'chat/direct.html',context)
   
def chatbox(request, username):
    pass

@login_required
@csrf_exempt
def load_chat(request):
    user = request.user.pk
    # to_user = request.POST.get('to_user')
    thread_id = request.POST.get('thread_id')
    # to_user_pk = User.objects.get(username=to_user)
    # threads = ThreadChat.objects.filter(Q(user_id=user)|Q(to_user_id=user),Q(user_id=to_user)|Q(to_user_id=to_user))
    threads = ThreadChat.objects.filter(pk=int(thread_id))

    if threads.exists():
        # messages = Message.objects.filter(thread_id=threads[0].id).update(is_read=True)
        testing = Message.objects.filter(thread_id=thread_id).values('pk','sender__pk','sender__username','body','date','is_read').order_by('date')
        
        # data = []
        # for message in messages:
        #     user = message.user
            
    # if messages.exists():
        # list_messages = serializers.serialize('json',testing)
        
        return JsonResponse({'data':list(testing)}, safe=False)
    else:
        return JsonResponse({})

@csrf_exempt
def create_chat(request):
    from_user = request.user.pk

    to_user = request.POST.get('to_user')
    # to_user_pk = User.objects.get(username=to_user)
    cek_id = ThreadChat.objects.select_related('user','to_user').filter(Q(user_id=from_user) | Q(user_id=to_user), Q(to_user_id=to_user) | Q(to_user_id=from_user))
    # threads = serializers.serialize('json', cek_id)
    if cek_id.exists():
        threads = cek_id.values('pk','user__pk','user__username','to_user__pk','to_user__username')
        return JsonResponse({'data':list(threads)}, safe=False)
    else:
        threads = ThreadChat.objects.create(user_id=from_user, to_user_id=to_user)

        return JsonResponse({'success':'Save!'})

@csrf_exempt
def is_read_chat(request):
    from_user = request.user.pk
    # thread_id = request.POST.get('user')
    # print(thread_id)
    to_user = request.POST.get('user')
    # threads = ThreadChat.objects.filter(pk=int(thread_id))
    threads = ThreadChat.objects.filter(Q(user_id=from_user) | Q(user_id=to_user), Q(to_user_id=to_user) | Q(to_user_id=from_user))
    try:
        if threads.exists():
            # messages = Message.objects.filter(thread_id=threads[0].id).update(is_read=True)
            messages = Message.objects.filter(thread_id=threads[0]).update(is_read=True)
            
            return JsonResponse({'data':'Done'})
    except ThreadChat.DoesNotExist:
        return JsonResponse({'error':'Data Tidak ditemukan!'})


@csrf_exempt
def load_read(request):
    from_user = request.user.pk
    to_user = request.POST.get('to_user')
    
    threads = ThreadChat.objects.filter(Q(user_id=from_user) | Q(user_id=to_user), Q(to_user_id=to_user) | Q(to_user_id=from_user))
    try:
        if threads.exists():
            pesan = Message.objects.filter(thread_id=threads[0].id).filter(is_read=False).values('sender_id','is_read','thread__user','thread__to_user')
            # pesan = serializers.serialize('json', [pesan])
            return JsonResponse({'data':list(pesan)}, safe=False)
    except ThreadChat.DoesNotExist:
        return JsonResponse({'error':'Data Not Found!'})

@csrf_exempt
def save_chat(request):
    user = request.user.pk
    thread_id = request.POST.get('thread_id')
    # to_user = request.POST.get('to_user')
    body = request.POST.get('pesan')
    # to_user_pk = User.objects.get(username=to_user)
    cek_id = ThreadChat.objects.filter(pk=int(thread_id))
    
    if cek_id.exists():  
        _ = Message.objects.create(thread_id=int(thread_id), sender_id=user, body=body)
        last_pesan = Message.objects.filter(thread_id=int(thread_id)).order_by('-date')[0]
        pesan = serializers.serialize('json', [last_pesan])

        return JsonResponse({'data':pesan})


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username = self.kwargs.get("username")
        obj, created = Thread.objects.get_or_new(self. request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)
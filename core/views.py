from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login
# from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from django.contrib import messages

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username, password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, "username or password not correct")
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html',{'form':form})

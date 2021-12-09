from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
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
        form = AuthenticationForm()
    return render(request, 'registration/login.html',{'form':form})

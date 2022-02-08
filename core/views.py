from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib import messages

# User = get_user_model()

@csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            msg = "Invalid Credentials"
    else:
        form = LoginForm()
        
    return render(request, 'registration/signin.html',{'form':form, 'msg':msg})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_password(request, pk):
    msg = None
    
    # pk = request.POST.get('id_pembina')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    
    if (password1 != password2) or (password1, password2) is None:
        msg = "Password tidak sama"
        return JsonResponse({'error':msg, 'status':400})
    else:
        password = make_password(password1, hasher='default')
        
        User.objects.filter(id=pk).update(password=password)
        return JsonResponse({'success':'Password berhasil diganti','status':200})

@login_required
def delete_user(request, pk):
    try:
        u = User.objects.get(pk=pk)
        u.delete()
        return JsonResponse({'msg':'done'})
    except User.DoesNotExist:
        return JsonResponse({'msg':'User Tidak di Temukan'})
    except Exception as e:
        return JsonResponse({'msg':e.message})

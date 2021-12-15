from .models import Informasi, Profile
# from .models import Profile

def info_context(request):
    user = Profile.objects.select_related('username').filter(username__username=request.user)
    if user.exists():
        datas = Informasi.objects.select_related('npp').filter(npp__pembina__username__username=request.user)
        return {'info':datas}
    else:
        datas = Informasi.objects.select_related('npp').filter(npp__npp=request.user)
        return {'info':datas}
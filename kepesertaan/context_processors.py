from .models import Informasi, Profile
from django.db.models import Q
# from .models import Profile

def info_context(request):
    try:
        kepala = Profile.objects.select_related('username','jabatan').filter(Q(jabatan__pk=1) | Q(jabatan__pk=2),username__username=request.user)
        if kepala.exists:
            datas = Informasi.objects.all()
            return {'info':datas, 'kepala':kepala}
        else:
            datas = Informasi.objects.select_related('user').filter(Q(user__username=request.user) | Q(user__username=kepala[0].username.username))
            return {'info':datas, 'kepala':kepala}
    except:
        pass
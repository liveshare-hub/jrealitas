from django.db.models import Q
from .models import approval_bak

def info_kunjungan(request):
    if request.user.is_authenticated:
        visits = approval_bak.objects.select_related('berita_acara').filter(Q(berita_acara__petugas__username__username=request.user) | Q(berita_acara__to_perusahaan__npp=request.user), status=0)
        context = {
            'visits':visits,
            'jumlah':visits.count()
        }
        return context
    return {}
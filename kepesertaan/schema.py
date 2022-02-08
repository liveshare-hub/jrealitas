import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import Jabatan, Profile, Bidang, Perusahaan

from django.contrib.auth.models import User

class JabatanType(DjangoObjectType):
    class Meta:
        model = Jabatan

class BidangType(DjangoObjectType):
    class Meta:
        model = Bidang

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class PerusahaanType(DjangoObjectType):
    class Meta:
        model = Perusahaan

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_jabatan = graphene.List(JabatanType)
    all_bidang = graphene.List(BidangType)
    all_jabatans = graphene.List(JabatanType, id=graphene.ID())
    all_npp = graphene.List(PerusahaanType)
    all_npp_pembina = graphene.List(PerusahaanType)
    all_profile = graphene.List(ProfileType)
    all_users = graphene.List(UserType)
    all_pembina_bidang = graphene.List(ProfileType)

    def resolve_all_jabatan(root, info, **kwargs):
        if info.context.user.is_authenticated:
            return Jabatan.objects.all()
        else:
            return Jabatan.objects.none

    def resolve_all_bidang(root, info, **kwargs):
        if info.context.user.is_authenticated:
            return Bidang.objects.all()
        else:
            return Bidang.objects.none

    def resolve_all_jabatans(root, info, id):
        if info.context.user.is_authenticated:
            return Jabatan.objects.select_related('bidang').filter(bidang__pk=id)
        else:
            return Jabatan.objects.none

    def resolve_all_profile(root, info):
        if info.context.user.is_authenticated:
            jabatan = Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=701)
            return Profile.objects.select_related('username','jabatan','kode_kantor').all().exclude(jabatan)

    def reslove_all_pembina_bidang(root, info):
        if info.context.user.is_authenticated:
            return Profile.objects.select_related('username','jabatan').all().exclude(username__username=info.context.user)

    def resolve_all_npp(root, info):
        if info.context.user.is_authenticated:
            return Perusahaan.objects.select_related('username','pembina').all()

    def resolve_all_npp_pembina(root, info):
        user = info.context.user
        if user.is_authenticated:
            return Perusahaan.objects.select_related('username','pembina').filter(pembina__username__username=user)

schema = graphene.Schema(query=Query)
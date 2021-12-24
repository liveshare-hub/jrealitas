import graphene
from graphene_django import DjangoObjectType
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
    all_profile = graphene.List(ProfileType)
    all_users = graphene.List(UserType)

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
            return Profile.objects.select_related('username','jabatan','kode_kantor').all().exclude(jabatan_id=3)

    def resolve_all_npp(root, info):
        if info.context.user.is_authenticated:
            return Perusahaan.objects.select_related('username','pembina').all()

schema = graphene.Schema(query=Query)
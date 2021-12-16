import graphene
from graphene_django import DjangoObjectType
from .models import Jabatan, Profile, Bidang

class JabatanType(DjangoObjectType):
    class Meta:
        model = Jabatan

class BidangType(DjangoObjectType):
    class Meta:
        model = Bidang

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class Query(graphene.ObjectType):
    all_jabatan = graphene.List(JabatanType)
    all_bidang = graphene.List(BidangType)
    all_profile = graphene.List(ProfileType)

    def resolve_all_jabatan(self, info, **kwargs):
       
        return Jabatan.objects.all()

    def resolve_all_bidang(self, info, **kwargs):
        return Bidang.objects.all()

    def resolve_all_profile(self, info):
        return Profile.objects.all()

schema = graphene.Schema(query=Query)
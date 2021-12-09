import graphene
from graphene_django import DjangoObjectType
from .models import Jabatan

class JabatanType(DjangoObjectType):
    class Meta:
        model = Jabatan


class Query(graphene.ObjectType):
    all_jabatan = graphene.List(JabatanType)

    def resolve_all_jabatan(self, info):
        print(info.context.jabatan)
        return Jabatan.objects.all()

schema = graphene.Schema(query=Query)
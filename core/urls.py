from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

urlpatterns = [
    path('', include('kepesertaan.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
]

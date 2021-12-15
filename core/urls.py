from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from .views import login_view, logout_view, edit_password

from graphene_django.views import GraphQLView

urlpatterns = [
    path('', include('kepesertaan.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('ganti/password/<int:pk>', edit_password, name='edit-password'),
    path('admin/', admin.site.urls),
]

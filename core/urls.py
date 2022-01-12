from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from core.settings import MEDIA_ROOT

from .views import login_view, logout_view, edit_password

from graphene_django.views import GraphQLView

urlpatterns = [
    path('', include('kepesertaan.urls')),
    path('chat/', include('chat.urls')),
    path('kunjungan/', include('kunjungan.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('ganti/password/<int:pk>', edit_password, name='edit-password'),
    path('admin/', admin.site.urls),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
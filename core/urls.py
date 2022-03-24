from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# from core.settings import MEDIA_ROOT

from .views import delete_user, login_view, logout_view, edit_password

from graphene_django.views import GraphQLView

urlpatterns = [
    path('', include('kepesertaan.urls')),
    path('chat/', include('chat.urls')),
    path('mychats/', include('mychats.urls')),
    path('kunjungan/', include('kunjungan.urls')),
    path('admin-page/', include('admin_page.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('ganti/password/<int:pk>', edit_password, name='edit-password'),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"), name="reset_password"),
    path('accounts/reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_password_confirmation.html"), name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('hapus/user/<int:pk>', delete_user, name='hapus-user'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

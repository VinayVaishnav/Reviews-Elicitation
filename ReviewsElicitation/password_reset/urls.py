from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'password_reset'

urlpatterns = [
    path('', views.password_reset_request, name='request'),
    path('confirm/<uidb64>/<token>/', views.password_reset_confirm, name='confirm'),
    path('done/', views.password_reset_done, name='done'),
    path('invalid/', views.password_reset_invalid, name='invalid'),
    path('sent/', views.password_reset_sent, name='sent')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

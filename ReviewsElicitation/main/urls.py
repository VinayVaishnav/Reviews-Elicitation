from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('',views.login,name='login'),
    path('signup//',views.signup, name='signup'),
    path('home/',views.home,name='home'),
    path('verify/',views.verify,name='verify'),
    path('logout/',views.logout,name='logout'),
    path('update/',views.update,name='update'),
    path('search/',views.search,name='search'),
    path('user/<str:username>/',views.user,name='user'),
    path('edit/<int:review_id>',views.edit,name='edit'),
    path('delete/<int:review_id>',views.delete,name='delete')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

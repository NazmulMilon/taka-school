from django.urls import path
from .views import user_login, logout

from django.urls import path

app_name = 'authentication'

urlpatterns = [
    path('admin/', user_login, name='admin-login'),
    path('login/', user_login, name='user-login'),
    path('logout/', logout, name='logout'),
]






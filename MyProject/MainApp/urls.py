
from django.urls import path, include

from .views import *

# nombre de la app
# appname = "NotMLApp"

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/cursos', dashboard_cursos, name='dashboard_cursos'),
    path('dashboard/enviar_mensaje/', enviar_mensaje, name='enviar_mensaje'),

    path('cursos/', cursos, name='cursos'),
    path('curso/<id_categoria>', cursos_categoria, name='cursos_categoria'),

    path('accounts/login', login_request, name="login"),
    path('accounts/register', register_request, name="register"),
    path('accounts/logout', logout_request, name="logout"),
    path('accounts/profile', profile, name="profile"),
]
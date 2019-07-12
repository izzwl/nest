from django.urls import path

from . import views00

app_name = 'authnest'

urlpatterns = [
    path('login/',views00.login, name="login"),
    path('logout/',views00.logout, name="logout"),
]

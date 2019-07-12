from django.urls import path

from . import views00

app_name = 'purchasing'

urlpatterns = [
    path('in71/',views00.in71, name="in71"),
    path('in72/',views00.in72, name="in72"),
    path('in73/',views00.in73, name="in73"),
    path('in74/',views00.in74, name="in74"),
    path('in75/<int:in73_id>/',views00.in75, name="in75"),
    path('in76/',views00.in76, name="in76"),
    path('in77/',views00.in77, name="in77"),

    path('in71/',views00.in71, name="in71"),

]

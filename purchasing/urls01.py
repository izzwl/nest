from django.urls import path

from . import views01

app_name = 'purchasing-v1'

urlpatterns = [
    path('in71/list',views01.in71_list, name="in71_list"),
    path('in71/detail/<int:pk>/',views01.in71_detail, name="in71_detail"),
    path('in71/add/',views01.in71_add, name="in71_add"),
    path('in71/change/<int:pk>/',views01.in71_change, name="in71_change"),
    path('in71/delete/<int:pk>/',views01.in71_delete, name="in71_delete"),
    path('in71/approve/<int:pk>/',views01.in71_approve, name="in71_approve"),
    path('in71/print/<int:pk>/',views01.in71_print, name="in71_print"),
    path('in71/in72/in73/prn/',views01.in71_in72_in73_prn_get, name="in71_in72_in73_prn_get"),

    path('in72/<int:fk>/list',views01.in72_list, name="in72_list"),
    path('in72/<int:fk>/add/',views01.in72_add, name="in72_add"),
    path('in72/<int:fk>/change/<int:pk>/',views01.in72_change, name="in72_change"),
    path('in72/<int:fk>/delete/<int:pk>/',views01.in72_delete, name="in72_delete"),
    path('in72/<int:fk>/approve/<int:pk>/',views01.in72_approve, name="in72_approve"),
    path('in72/<int:fk>/approve_all',views01.in72_approve_all, name="in72_approve_all"),

    path('in73/<int:fk>/list',views01.in73_list, name="in73_list"),
    path('in73/<int:fk>/add/<int:ook>',views01.in73_add, name="in73_add"),


]

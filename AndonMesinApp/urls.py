from django.urls import path
from . import views

urlpatterns = [
    path('', views.ViewDashboard.as_view(), name='dashboard'),

    # Kategori
    path('category/register/', views.RegisterKategori.as_view(), name='register_kategori'),
    path('category/list/', views.ListKategori.as_view(), name='list_kategori'),

    # Mesin
    path('machine/register/', views.RegisterMesin.as_view(), name='register_mesin'),
    path('machine/list/', views.ListMesin.as_view(), name='list_mesin'),

    # Departemen
    path('department/register/', views.RegisterDepartemen.as_view(), name='register_departemen'),
    path('department/list/', views.ListDepartemen.as_view(), name='list_departemen'),

    # Role
    path('role/register/', views.RegisterPeran.as_view(), name='register_role'),
    path('role/list/', views.ListPeran.as_view(), name='list_role'),


    # esp endpoint
    path('response/esp32-endpoint/', views.ReceiveData, name='control_receive'),
]
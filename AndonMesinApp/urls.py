from django.urls import path
from . import views

urlpatterns = [
    path('', views.ViewDashboard.as_view(), name='dashboard'),
    # htmx response
    path('async-mesin-card/', views.AsyncMesinCard, name='async_card'),
    path('async-list-downtime/', views.AsyncDowntimeList, name='async_list_dt'),

    # Kategori
    path('category/register/', views.RegisterKategori.as_view(), name='register_kategori'),
    path('category/update/<int:pk>', views.UpdateKategori.as_view(), name='update_kategori'),
    path('category/list/', views.ListKategori.as_view(), name='list_kategori'),

    # Mesin
    path('machine/register/', views.RegisterMesin.as_view(), name='register_mesin'),
    path('machine/update/<int:pk>', views.UpdateMesin.as_view(), name='update_mesin'),
    path('machine/list/', views.ListMesin.as_view(), name='list_mesin'),

    # Departemen
    path('department/register/', views.RegisterDepartemen.as_view(), name='register_departemen'),
    path('department/update/<int:pk>', views.UpdateDepartemen.as_view(), name='update_departemen'),
    path('department/list/', views.ListDepartemen.as_view(), name='list_departemen'),

    # Downtime
    path('downtime/list/', views.ListDowntime.as_view(), name='list_downtime'),

    # Role
    path('role/register/', views.RegisterPeran.as_view(), name='register_role'),
    path('role/update/<int:pk>', views.UpdatePeran.as_view(), name='update_role'),
    path('role/list/', views.ListPeran.as_view(), name='list_role'),

    # esp endpoint
    # path('response/esp32-endpoint/', views.ReceiveData, name='control_receive'),
    path('response/esp32-endpoint/', views.Esp32EndpointView.as_view(), name='esp32-endpoint'),
]
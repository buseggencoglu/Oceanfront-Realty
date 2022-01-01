from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('house/list/', views.house_list, name='house_list'),
    path('houses/available', views.available_houses, name='available_houses'),
    path('users/', views.users, name='users'),
    path('profile/<int:pk>', views.view_profile, name='profile'),
    path('profile/edit/<int:pk>', views.edit_profile, name='edit_profile'),
    path('reservations/list', views.reservation_list, name='reservation_list'),
    path('reservations/<int:house_id>/<str:location>/<str:pickUpDate>/<str:returnDate>',
         views.create_reservation, name='reservation_create'),
    path('reservation/approve', views.complete_reservation, name='reservation_approve'),
    path('contact/', views.contact, name='contact'),
    path('reservations/housedealer', views.view_my_reservation_housedealer, name='housedealer_reservations'),
    path('reservations/customer', views.view_my_reservation_customer, name='customer_reservations'),
    path('house/create/<int:branch_page>', views.create_house, name='create_house'),
    path('house/create/', views.create_house, name='create_house'),
    path('house/update/<int:pk>/<int:branch_page>', views.house_update, name='house_update'),
    path('house/delete/<int:pk>', views.house_delete, name='house_delete'),
    path('house/update/<int:pk>', views.house_update, name='house_update'),
    path('reservations/delete/customer/<int:pk>', views.reservation_delete, name='reservation_delete'),
    path('admin/dashboard', views.total_house_list, name='total_house_list'),
    path('reservations/admin', views.reservation_list, name='reservation_list'),
    path('admin/user/approve/<int:pk>', views.house_dealer_approve, name='reservation_list'),
    path('branch/add', views.add_branch, name='add_branch'),
    path('branch/list', views.branch_list, name='branch_list'),
    path('branch/delete/<int:pk>', views.branch_delete, name='branch_delete'),
    path('branch/update/<int:pk>', views.branch_update, name='branch_update'),
    path('branch/branch_house_list/<int:pk>', views.branch_house_list, name='branch_house_list'),
    path('admin/housedealerdelete/<int:pk>', views.houseDealer_delete, name='houseDealer_delete'),
    path('admin/user/delete/<int:pk>', views.house_dealer_reject, name='house_dealer_reject'),
    path('delete/notification/<int:pk>', views.delete_notification, name='delete_notification'),
    path('reservations/customer/history', views.view_my_reservation_customer_history, name='my_reservation_customer_history'),
    path('reservations/housedealer/history', views.view_my_reservation_housedealer_history, name='my_reservation_housedealer_history'),
    path('reservations/admin/history', views.view_my_reservation_admin_history, name='my_reservation_admin_history'),



]

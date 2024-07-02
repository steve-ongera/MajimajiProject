
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pay/', views.tenant_payment_status, name='payment_status'),
    path('add-payment/', views.add_payment, name='add_payment'),
    path('edit-payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('my-payment-history/', views.tenant_payment_history, name='tenant_payment_history'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tenants/', views.tenant_list, name='tenant_list'),
     path('tenant/<int:tenant_id>/', views.tenant_detail, name='tenant_detail'),
    path('tenant/<int:tenant_id>/update/', views.tenant_update, name='tenant_update'),
    path('tenant/<int:tenant_id>/delete/', views.tenant_delete, name='tenant_delete'),
    path('tenant/<int:tenant_id>/maintenance/request/', views.maintenance_request_create, name='maintenance_request_create'),
    path('maintenance/requests/', views.maintenance_request_list, name='maintenance_request_list'),
    path('maintenance/request/<int:request_id>/respond/', views.respond_to_request, name='respond_to_request'),
    path('add_tenant', views.add_tenant , name='add_tenant'),
    path('add_tenant_databse', views.add_tenant_databse , name='add_tenant_databse'),
    path('user_list', views.user_list , name='user_list'),
    path('add_house', views.add_house , name='add_house'),
    path('house_list', views.house_list , name='house_list'),
    path('search-tenant/', views.search_tenant, name='search_tenant'),
    #######3
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path('homepage', views.homepage, name='homepage'),
    path('process/', views.process_query, name='process_query'),
   
    
]


from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('admin_view', views.admin, name='admin_index' ),
    path('profile', views.profile, name='profile'),
    path ('login_check',views.check, name='login_check'),
    path ('log_out', views.log_out, name='log_out'),
    path ('checklog',views.check_log,name="checklog"),
    path ('lab_incharge',views.lab_incharge,name="lab_incharge"),
    path('update_movement',views.update_movement,name="update_movement"), 
    #path ('clerk',views.clerk, name='clerk'),
    path('admin_statistics',views.admin_statistics,name="admin_statistics"),
    path ('movements',views.movements,name="movements"),
    path ('request_incharge',views.request_incharge,name="request_incharge"),
    path ('request_admin',views.request_admin,name="request_admin"),
    #path ('update_profile',views.update_profile,name="update_profile") 
]
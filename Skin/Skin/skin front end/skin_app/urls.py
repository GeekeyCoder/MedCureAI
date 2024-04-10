from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path(r'^submit/$',views.submit,name='submit'),
    path(r'^signup/$',views.signup, name='signup'),
    path(r'^login/$',views.login, name='login'),
    path(r'^logout/$',views.logout, name='logout'),
    path(r'^home/$',views.dashboard, name='dashboard')
]
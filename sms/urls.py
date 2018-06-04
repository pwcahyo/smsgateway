from django.conf.urls import url 
from django.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^home/$', views.home, name='home'),
    url(r'^home/delete/(?P<pk>\d+)$', views.delete, name='delete'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='user/login.html')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
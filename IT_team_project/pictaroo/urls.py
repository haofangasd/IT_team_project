from django.conf.urls import url
from pictaroo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register/$', views.register, name='register'), #Map the registration URL


    url(r'^my_account/$', views.my_account, name = 'my_account'),

    url(r'^my_comments/$', views.my_comments, name = 'my_comments'),

    url(r'^my_uploads/$', views.my_uploads, name = 'my_uploads'),

    url(r'^my_favourites/', views.my_favourites, name = 'my_favourites'),



]
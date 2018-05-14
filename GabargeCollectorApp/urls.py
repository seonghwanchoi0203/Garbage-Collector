"""GabargeCollectorApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from garbage import views as garbage_views
from userprof import views as userprof_views

urlpatterns = [
    url('admin/', admin.site.urls),
    #url('accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', garbage_views.home, name='home'),
	url('home/', garbage_views.home, name='home'),
	url('about',garbage_views.about,name = 'about'),
	url('profile',userprof_views.profile,name = 'profile'),
    url('contact',garbage_views.contact,name = 'contact'),
    url('new_item',garbage_views.new_item,name = 'new_item'),
    url('edit_item', garbage_views.edit_item, name='edit_item'),
    url('watch', garbage_views.watch, name='watch'),
    url('editBio',userprof_views.editBio,name = 'editBio'),
    url('sendEmail',garbage_views.sendEmail, name = 'sendEmail'),
    url('ItemDetails',garbage_views.ItemDetails, name = 'ItemDetails'),
    url('sell', userprof_views.sell, name='sell'),
    url('orderComplete', garbage_views.orderComplete, name = 'orderComplete'),
    url('inAppTransaction', garbage_views.inAppTransaction, name = 'inAppTransaction')

]

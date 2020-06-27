"""sentiment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from texteye.views import index, feedback, predict, store_feedback, applications

urlpatterns = [
    path('texteye/', include('texteye.urls')),
    path('admin/', admin.site.urls),
    url('^$', index, name='homepage'),
    url(r'^applications', applications, name='applications'),
    url(r'^feedback', feedback, name='feedback'),
    url('predict', predict, name='predict'),
    url('store_feedback',store_feedback, name='store feedback')

]

urlpatterns += staticfiles_urlpatterns()

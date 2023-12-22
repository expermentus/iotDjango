"""
URL configuration for iotFDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from FDjango.views import loadBase, alter_light, alter_light_all, turn_off_light, turn_off_light_all


urlpatterns = [
    path('', loadBase, name='home'),  # This is for the root path
    path('alter_light_all/', alter_light_all, name='alter_light_all'),
    path('alter_light/', alter_light, name='alter_light'),
    path('turn_off_light_all/', turn_off_light_all, name='turn_off_light_all'),
    path('turn_off_light/', turn_off_light, name='turn_off_light'),
    path('base/', loadBase, name='load_base'),
    path('admin/', admin.site.urls),
]
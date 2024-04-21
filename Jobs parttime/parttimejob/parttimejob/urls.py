"""
URL configuration for partimejob project.

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
from parttimeapp import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name='home'),
    path('login/',views.login_user, name= 'login'),
    path('signup/',views.signup, name= 'signup'),
    path('logout/',views.logoutpage, name= 'logout'),
    path('addjob/',views.addjob, name= 'addjob'),
    path('applyjob/<int:job_id>/',views.applyjob, name= 'applyjob'),
    path('update_job/<int:job_id>/', views.update_job, name='update_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
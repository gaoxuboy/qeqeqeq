"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app01 import views
from django.views.static import serve
from blog import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^blog/', include('app01.urls')),
    url(r'^login/', views.log_in),
    url(r'^imger/', views.imger),  # 验证码路径
    url(r'^dell/', views.dell),
    url(r'^register/', views.register),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 图像认证路径
    url(r'^poll/', views.poll),
    url(r'^comment/', views.comment),
    url(r'^updown/', views.updown),
    url(r'^addarticle/', views.addarticle),
    url(r'^filename/', views.filename),
    url(r'^management/', views.management),
    url(r'^del/', views.del2),
    url(r'^commentup/', views.commentup),
    url(r'^mima/', views.mima),

]

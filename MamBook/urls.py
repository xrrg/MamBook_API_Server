"""The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from django.conf.urls import url
from MamBook import views

urlpatterns = [
    url(r'baby_achievement.json/(?P<baby_id>[0-9]+)/(?P<request_token>.*)/$', views.get_baby_achievement),
    url(r'login/', views.log_in),
    url(r'logout/', views.log_out),
    url(r'register/', views.register),
    url(r'achievement.json/', views.get_achievement),
    url(r'category.json/', views.get_category),
    url(r'progress.json/', views.get_progress),
    url(r'selfdevelopment.json/', views.get_selfdevelopment),
    url(r'', views.initialize),
]


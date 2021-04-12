"""lab_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include

from rest_framework import routers
import iur.views
import cat.views

router = routers.DefaultRouter()
router.register(r'users',iur.views.UserViewSet)
router.register(r'groups',iur.views.GroupViewSet)
router.register(r'uuts',iur.views.UutViewSet)
router.register(r'platforms',iur.views.PlatformViewSet)
router.register(r'platformconfigs',iur.views.PlatformConfigViewSet)
router.register(r'uutphases',iur.views.UutPhaseViewSet)
router.register(r'uutstatus',iur.views.UutStatusViewSet)
router.register(r'platformphases',iur.views.PlatformPhaseViewSet)
router.register(r'tasks',cat.views.TaskViewSet)
router.register(r'scripts',cat.views.ScriptViewSet)
router.register(r'aps',cat.views.ApViewSet)
router.register(r'taskstatus',cat.views.TaskStatusViewSet)
router.register(r'taskissues',cat.views.TaskIssueViewSet)
router.register(r'powerstates',cat.views.PowerStateViewSet)


urlpatterns = [
    path('api/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', admin.site.urls),
    path('iur/',include('iur.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

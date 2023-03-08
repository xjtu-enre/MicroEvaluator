from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('project', views.ProjectViewSet)
router.register('version', views.VersionProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('test/', views.test),
]

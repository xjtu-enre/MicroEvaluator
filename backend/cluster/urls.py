from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('cluster', views.ClusterDatasViewSet)
router.register('catelogues', views.CatelogueDatasViewSet)
router.register('cateloguesTreeMap', views.CatelogueTreeMapDatasViewSet)
# router.register('sectionNodes', views.SectionNodesViewSet)
# router.register('sectionEdges', views.SectionEdgesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('cluster/', views.get_cluster_data, name='cluster')
]

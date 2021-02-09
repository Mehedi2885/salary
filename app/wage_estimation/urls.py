from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import WageEstimationViewSet

router = DefaultRouter()
router.register('wage-estimation', WageEstimationViewSet,
                basename="wage-estimation")  # /api/wage-estimation

urlpatterns = [
    url(r'', include(router.urls))
]

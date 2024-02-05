from rest_framework.routers import DefaultRouter

from ricette.views import RicettaViewSet

router = DefaultRouter()

router.register(r'', RicettaViewSet, basename='ricette')

urlpatterns = router.urls

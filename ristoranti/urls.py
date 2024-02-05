from rest_framework.routers import DefaultRouter

from ristoranti.views import RistoranteViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'', RistoranteViewSet, basename='ristoranti')

urlpatterns = router.urls

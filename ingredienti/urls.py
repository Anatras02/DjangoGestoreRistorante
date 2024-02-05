from rest_framework.routers import DefaultRouter

from ingredienti.views import IngredienteViewSet

router = DefaultRouter()

router.register(r'', IngredienteViewSet, basename='ingredienti')

urlpatterns = router.urls

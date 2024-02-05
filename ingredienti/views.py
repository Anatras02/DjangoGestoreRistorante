from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredienti.models import Ingrediente
from ingredienti.serializers import IngredienteSerializer
from ricette.serializers import RicettaSerializer


class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

    @swagger_auto_schema(
        operation_description="Lista delle ricette che contengono un ingrediente",
        responses={200: IngredienteSerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def ricette(self, request, pk=None):
        ingrediente = self.get_object()
        ricette = ingrediente.ricette.all()
        serializer = RicettaSerializer(ricette, many=True, context={'request': request})

        return Response(serializer.data)

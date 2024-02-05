from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredienti.models import Ingrediente
from ingredienti.serializers import IngredienteSerializer
from ricette.models import Ricetta
from ricette.serializers import RicettaSerializer
from ristoranti.models import Ristorante
from ristoranti.serializers import RistoranteSerializer


# Create your views here.
class RistoranteViewSet(viewsets.ModelViewSet):
    queryset = Ristorante.objects.all()
    serializer_class = RistoranteSerializer

    @swagger_auto_schema(
        operation_description="Lista delle ricette di un ristorante",
        responses={200: RicettaSerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def ingredienti(self, request, pk=None):
        ristorante = self.get_object()

        ingredienti_ids = Ricetta.objects.filter(ristoranti=ristorante).values_list('ingredienti', flat=True).distinct()
        ingredienti = Ingrediente.objects.filter(id__in=ingredienti_ids)

        serializer = IngredienteSerializer(ingredienti, many=True, context={'request': request})

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Lista delle ricette di un ristorante",
        responses={200: RicettaSerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def ricette(self, request, pk=None):
        ristorante = self.get_object()

        ricette = Ricetta.objects.filter(ristoranti=ristorante)
        serializer = RicettaSerializer(ricette, many=True, context={'request': request})

        return Response(serializer.data)

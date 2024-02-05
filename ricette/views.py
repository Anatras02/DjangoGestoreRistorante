# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredienti.serializers import IngredienteSerializer
from ricette.models import Ricetta
from ricette.serializers import RicettaSerializer
from ristoranti.serializers import RistoranteSerializer


class RicettaViewSet(viewsets.ModelViewSet):
    queryset = Ricetta.objects.all()
    serializer_class = RicettaSerializer

    @swagger_auto_schema(
        operation_description="Lista degli ingredienti di una ricetta",
        responses={200: IngredienteSerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def ingredienti(self, request, pk=None):
        ricetta = self.get_object()
        ingredienti = ricetta.ingredienti.all()
        serializer = IngredienteSerializer(ingredienti, many=True, context={'request': request})

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Lista dei ristoranti di una ricetta",
        responses={200: RicettaSerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def ristoranti(self, request, pk=None):
        ricetta = self.get_object()
        ristoranti = ricetta.ristoranti.all()
        serializer = RistoranteSerializer(ristoranti, many=True, context={'request': request})

        return Response(serializer.data)

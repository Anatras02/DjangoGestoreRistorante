from django.urls import reverse
from rest_framework import serializers
from rest_framework.request import Request

from ricette.models import Ricetta


class RicettaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ricetta
        fields = ('id', 'nome', 'descrizione', 'ingredienti')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request: Request = self.context.get('request')

        representation['ingredienti'] = [
            request.build_absolute_uri(
                reverse('ingredienti-detail', args=[ingrediente.id])
            )
            for ingrediente in instance.ingredienti.all()
        ]

        return representation

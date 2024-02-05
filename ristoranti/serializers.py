from django.urls import reverse
from rest_framework import serializers
from rest_framework.request import Request

from ristoranti.models import Ristorante


class RistoranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ristorante
        fields = ('id', 'nome', 'indirizzo', 'email', 'cellulare', 'sito_web', 'ricette')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request: Request = self.context.get('request')

        representation['ricette'] = [
            request.build_absolute_uri(
                reverse('ricette-detail', args=[ricetta.id])
            )
            for ricetta in instance.ricette.all()
        ]

        return representation

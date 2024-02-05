from rest_framework import serializers

from ingredienti.models import Ingrediente


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ('id', 'nome', 'unita_di_misura')

import unittest

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from ingredienti.models import Ingrediente
from ingredienti.views import IngredienteViewSet
from ricette.models import Ricetta


class TestIngredienteViewSet(TestCase):
    INGREDIENTS = [
        {"nome": "Prova", "unita_di_misura": "Valore"},
        {"nome": "Prova2", "unita_di_misura": "Valore2"},
        {"nome": "Prova3", "unita_di_misura": "Valore3"},
    ]

    RECIPES = [
        {"nome": "Ricetta1", "descrizione": "Descrizione1"},
        {"nome": "Ricetta2", "descrizione": "Descrizione2"},
        {"nome": "Ricetta3", "descrizione": "Descrizione3"},
    ]

    @staticmethod
    def _create_default_ingredients():
        for dato in TestIngredienteViewSet.INGREDIENTS:
            Ingrediente.objects.create(**dato)

    @staticmethod
    def _create_recipes():
        for dato in TestIngredienteViewSet.RECIPES:
            Ricetta.objects.create(**dato)

    @staticmethod
    def _associate_ingredients_to_recipes():
        ricette = Ricetta.objects.all()
        ingredienti = Ingrediente.objects.all()

        for i, ricetta in enumerate(ricette):
            ricetta.ingredienti.add(ingredienti[i])

    def setUp(self):
        self.list_view = IngredienteViewSet.as_view({'get': 'list'})
        self.create_view = IngredienteViewSet.as_view({'post': 'create'})
        self.retrieve_view = IngredienteViewSet.as_view({'get': 'retrieve'})
        self.update_view = IngredienteViewSet.as_view({'put': 'update'})
        self.partial_update_view = IngredienteViewSet.as_view({'patch': 'partial_update'})
        self.delete_view = IngredienteViewSet.as_view({'delete': 'destroy'})
        self.ricette_view = IngredienteViewSet.as_view({'get': 'ricette'})

        self.factory = APIRequestFactory()
        self.url = '/ingredienti/'

        self._create_default_ingredients()
        self._create_recipes()
        self._associate_ingredients_to_recipes()

    def test_list_all(self):
        request = self.factory.get(self.url)
        response = self.list_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        for i, dato in enumerate(TestIngredienteViewSet.INGREDIENTS):
            self.assertEqual(dato["nome"], response.data[i]["nome"])
            self.assertEqual(dato["unita_di_misura"], response.data[i]["unita_di_misura"])

    def test_create(self):
        request = self.factory.post(self.url, {"nome": "Prova4", "unita_di_misura": "Valore4"})
        response = self.create_view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ingrediente.objects.count(), 4)

        self.assertEqual(Ingrediente.objects.get(nome="Prova4").unita_di_misura, "Valore4")

    def test_create_with_existing_name(self):
        request = self.factory.post(self.url, {"nome": "Prova", "unita_di_misura": "Valore"})
        response = self.create_view(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ingrediente.objects.count(), 3)

    def test_create_with_invalid_data(self):
        request = self.factory.post(self.url, {"nome": "Prova4"})
        response = self.create_view(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ingrediente.objects.count(), 3)

    def test_retrieve(self):
        request = self.factory.get(self.url + "1/")
        response = self.retrieve_view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, TestIngredienteViewSet.INGREDIENTS[0] | {"id": 1})

    def test_retrieve_not_found(self):
        request = self.factory.get(self.url + "4/")
        response = self.retrieve_view(request, pk=4)

        self.assertEqual(response.status_code, 404)

    def test_update(self):
        request = self.factory.put(
            self.url + "1/",
            {"nome": "ProvaModificata", "unita_di_misura": "ValoreModificato"}
        )
        response = self.update_view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingrediente.objects.get(pk=1).nome, "ProvaModificata")
        self.assertEqual(Ingrediente.objects.get(pk=1).unita_di_misura, "ValoreModificato")

    def test_partial_update(self):
        request = self.factory.patch(self.url + "1/", {"unita_di_misura": "Valore1"})
        response = self.partial_update_view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingrediente.objects.get(pk=1).unita_di_misura, "Valore1")

    def test_delete(self):
        request = self.factory.delete(self.url + "1/")
        response = self.delete_view(request, pk=1)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ingrediente.objects.count(), 2)

    def test_delete_not_found(self):
        request = self.factory.delete(self.url + "4/")
        response = self.delete_view(request, pk=4)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Ingrediente.objects.count(), 3)

    def test_ricette(self):
        request = self.factory.get(self.url + "1/ricette/")
        response = self.ricette_view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["nome"], "Ricetta1")

    def test_ricette_not_found(self):
        request = self.factory.get(self.url + "4/ricette/")
        response = self.ricette_view(request, pk=4)

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

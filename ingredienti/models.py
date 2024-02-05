from django.db import models


class Ingrediente(models.Model):
    nome = models.TextField(unique=True)
    unita_di_misura = models.TextField()

    def __str__(self):
        return self.nome

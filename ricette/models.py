from django.db import models


class Ricetta(models.Model):
    nome = models.TextField(unique=True)
    descrizione = models.TextField()

    ingredienti = models.ManyToManyField(
        'ingredienti.Ingrediente',
        related_name='ricette'
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Ricette'


from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Ristorante(models.Model):
    nome = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=100)
    email = models.EmailField()
    cellulare = PhoneNumberField()
    sito_web = models.URLField()

    ricette = models.ManyToManyField(
        'ricette.Ricetta',
        related_name='ristoranti'
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Ristoranti'
        unique_together = ('nome', 'indirizzo')

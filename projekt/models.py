from django.db import models
from django.utils import timezone
from django.conf import settings

class Firma(models.Model):
    nazwa_firmy = models.CharField(max_length=100)
    miasto = models.CharField(max_length=100)
    ulica = models.CharField(max_length=100)
    telefon = models.CharField(max_length=9)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwa_firmy

class Oferta(models.Model):
    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    branza = models.CharField(max_length=200)
    lokalizacja = models.CharField(max_length=100)
    wakat = models.CharField(max_length=100)
    wynagrodzenie = models.FloatField(default=0)
    opis = models.CharField(max_length=1000, blank=True)
    data_utworzenia = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.wakat

class Aplikant(models.Model):
    imie = models.CharField(max_length=100)
    wiek = models.IntegerField()
    wyksztalcenie = models.CharField(max_length=100)
    pochodzenie = models.CharField(max_length=100)


'''
class Odpowiedz_Na_Aplikacje(models.Model):

class Ankieta(models.Model):

class CV(models.Model):
'''
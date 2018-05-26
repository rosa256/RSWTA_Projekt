from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.conf import settings

class Firma(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='firma')
    nazwa_firmy = models.CharField(max_length=100)
    miasto = models.CharField(max_length=100)
    ulica = models.CharField(max_length=100)
    telefon = models.CharField(max_length=9)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.nazwa_firmy


class Oferta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oferta')
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
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='aplikant') # Powiązanie z Userami
    imie = models.CharField(max_length=100)
    wiek = models.IntegerField(blank=True, default=0)
    wyksztalcenie = models.CharField(max_length=100,blank=True, default='')
    telefon = models.CharField(max_length=20, blank=True, default='')
    miasto = models.CharField(max_length=100, blank=True,default='')
    panstwo = models.CharField(max_length=100,blank=True,default='')
    opis = models.TextField(blank=True, default='')

    def __str__(self):
        return self.user.username



'''
class Odpowiedz_Na_Aplikacje(models.Model):

class Ankieta(models.Model):

class CV(models.Model):
'''
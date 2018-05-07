from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

class Firma(models.Model):
    nazwa_firmy = models.CharField(max_length=100)
    miasto = models.CharField(max_length=100)
    ulica = models.CharField(max_length=100)
    telefon = models.CharField(max_length=9)
    email = models.EmailField(max_length=50)

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

class UserAplication(models.Model):
    user = models.OneToOneField(User, related_name='user') # Powiązanie z Userami

    imie = models.CharField(max_length=100)
    wiek = models.IntegerField(blank=True, default=0)
    wyksztalcenie = models.CharField(max_length=100,blank=True, default='')
    pochodzenie = models.CharField(max_length=100,blank=True, default='')
    telefon = models.CharField(max_length=20, blank=True, default='')
    miasto = models.CharField(max_length=100, blank=True,default='')
    panstwo = models.CharField(max_length=100,blank=True,default='')
    opis = models.TextField(blank=True, default='')

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserAplication(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

'''
class Odpowiedz_Na_Aplikacje(models.Model):

class Ankieta(models.Model):

class CV(models.Model):
'''
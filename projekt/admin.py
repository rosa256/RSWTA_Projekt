from django.contrib import admin
from .models import Oferta
from .models import Firma
from .models import UserAplication

admin.site.register(Oferta)
admin.site.register(Firma)
admin.site.register(UserAplication)
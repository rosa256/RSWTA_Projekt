from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from .models import Firma
from .models import Oferta
from .models import Aplikant

def oferta_list(request):
    oferta = Oferta.objects.filter(data_utworzenia__lte=timezone.now()).order_by('data_utworzenia')
    return render(request, 'projekt/oferta_list.html', {'oferta': oferta})

def oferta_detail(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    return render(request, 'projekt/oferta_detail.html', {'oferta': oferta})

def firma_list(request):
    firma = Firma.objects.all().order_by('nazwa_firmy')
    return render(request, 'projekt/firma_list.html', {'firma': firma})

def aplikant_list(request):
    aplikant = Aplikant.objects.all()
    return render(request, 'projekt/aplikant_list.html', {'aplikant': aplikant})


# Create your views here.

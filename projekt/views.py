from django.shortcuts import render, get_object_or_404, redirect
from .models import Firma, Oferta, Aplikant
from django.utils import timezone

from django.contrib.auth import authenticate, login
from  django.views import generic
from django.views.generic import View
from .forms import UserForm

from django.http import HttpResponse


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

def firma_detail(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    return render(request, 'projekt/firma_detail.html', {'firma': firma})

def aplikant_detail(request, pk):
    aplikant = get_object_or_404(Aplikant, pk=pk)
    return render(request, 'projekt/aplikant_detail.html', {'aplikant': aplikant})

def register_success(request):
    return render(request,'projekt/register_success.html')


class User_form_view(View):
    form_class = UserForm
    template_name = 'projekt/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form': form})

    def post(self, request):
            form = self.form_class(request.POST)

            if form.is_valid():

                user = form.save(commit=False)

                # cleaned (normalized) data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)

                if user is not None:

                    if user.is_active:
                        login(request, user)
                        return redirect('register_success')

            return render(request, self.template_name, {'form': form})

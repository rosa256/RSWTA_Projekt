from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from .models import Firma, Oferta, Aplikant, Aplikacja
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.views.generic import View
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, OfertaForm, CvForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def oferta_list(request):

    oferta = Oferta.objects.filter(data_utworzenia__lte=timezone.now()).order_by('data_utworzenia')
    request.session['is_aplikant_cv'] = 0
    request.session['branza_filter'] = 1
    request.session['wakat_filter'] = 1
    request.session['lokalizacja_filter'] = 1
    request.session['wynagrodzenie_filter'] = 1

    queryset = Oferta.objects.all()
    context = {
    "queryset":queryset,
    "oferta":oferta
    }

    if request.user.is_superuser:
        logout(request)
        return render(request, 'projekt/form.html', {})

    if request.user.is_authenticated():
        if(request.session['is_aplikant'] and Aplikant.objects.get(user_id=request.session['active_user_pk']).cv ): #User jest zalogowany jako aplikant i ma załadowane CV.
            print("MA CV")
            request.session['is_aplikant_cv']=1
    return render(request, 'projekt/oferta_list.html', context)


def oferta_detail(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    request.session['active_oferta_id'] = pk
    return render(request, 'projekt/oferta_detail.html', {'oferta': oferta})

def firma_list(request):
    request.session['nazwa_firmy_filter'] = 1
    request.session['miasto_filter'] = 1
    queryset = Firma.objects.all()
    print(queryset)
    context={
    "queryset":queryset
    }
    return render(request, 'projekt/firma_list.html',context)

def aplikant_list(request):
    request.session['wiek_filter'] = 1
    request.session['imie_filter'] = 1
    request.session['wyksztalcenie_filter'] = 1
    queryset = Aplikant.objects.all()
    context ={
        "queryset":queryset,
    }
    return render(request, 'projekt/aplikant_list.html', context)

def aplikant_list_filter_wiek(request):

    if(request.session['wiek_filter'] == 1):
        queryset = Aplikant.objects.all().order_by('wiek')
        request.session['wiek_filter'] = -1
    else:
        queryset = Aplikant.objects.all().order_by('-wiek')
        request.session['wiek_filter'] = 1

    print(queryset)
    context = {
        "queryset": queryset
    }
    return render(request, 'projekt/filters/aplikant/aplikant_list_filter_imie.html', context)

def aplikant_list_filter_imie(request):

    if (request.session['imie_filter'] == 1):
        queryset = Aplikant.objects.all().order_by('imie')
        request.session['imie_filter'] = -1
    else:
        queryset = Aplikant.objects.all().order_by('-imie')
        request.session['imie_filter'] = 1

    print(queryset)
    context = {
        "queryset": queryset
    }
    return render(request, 'projekt/filters/aplikant/aplikant_list_filter_imie.html', context)

def aplikant_list_filter_wyksztalcenie(request):

    if (request.session['wyksztalcenie_filter'] == 1):
        queryset = Aplikant.objects.all().order_by('wyksztalcenie')
        request.session['wyksztalcenie_filter'] = -1
    else:
        queryset = Aplikant.objects.all().order_by('-wyksztalcenie')
        request.session['wyksztalcenie_filter'] = 1

    print(queryset)
    context = {
        "queryset": queryset
    }
    return render(request, 'projekt/filters/aplikant/aplikant_list_filter_wyksztalcenie.html', context)


def firma_detail(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    return render(request, 'projekt/firma_detail.html', {'firma': firma})

def firma_list_filter_nazwa_firmy(request):
    if(request.session['nazwa_firmy_filter'] == 1):
        queryset = Firma.objects.all().order_by('nazwa_firmy')
        request.session['nazwa_firmy_filter'] = -1
    else:
        queryset=Firma.objects.all().order_by('-nazwa_firmy')
        request.session['nazwa_firmy_filter']=1

    print(queryset)
    context = {
        "queryset":queryset
    }
    return render(request, 'projekt/filters/firma/firma_list_filter_nazwa_firmy.html',context)

def firma_list_filter_miasto(request):
    if(request.session['miasto_filter'] == 1):
        queryset = Firma.objects.all().order_by('miasto')
        request.session['miasto_filter'] = -1
    else:
        queryset=Firma.objects.all().order_by('-miasto')
        request.session['miasto_filter']  = 1

    print(queryset)
    context = {
        "queryset":queryset
    }
    return render(request,'projekt/filters/firma/firma_list_filter_miasto.html',context)

def oferta_list_filter_branza(request):
    if(request.session['branza_filter'] ==1):
        queryset = Oferta.objects.all().order_by('branza')
        request.session['branza_filter'] = -1
    else:
        queryset=Oferta.objects.all().order_by('-branza')
        request.session['branza_filter'] = 1

    print(queryset)
    context = {
    'queryset':queryset
    }
    return render(request,'projekt/filters/oferta/oferta_list_filter_branza.html',context)

def oferta_list_filter_wakat(request):
    if(request.session['wakat_filter'] ==1):
        queryset = Oferta.objects.all().order_by('wakat')
        request.session['wakat_filter'] = -1
    else:
        queryset=Oferta.objects.all().order_by('-wakat')
        request.session['wakat_filter'] = 1

    print(queryset)
    context = {
    'queryset':queryset
    }
    return render(request,'projekt/filters/oferta/oferta_list_filter_wakat.html',context)

def oferta_list_filter_lokalizacja(request):
    if(request.session['lokalizacja_filter'] ==1):
        queryset = Oferta.objects.all().order_by('lokalizacja')
        request.session['lokalizacja_filter'] = -1
    else:
        queryset=Oferta.objects.all().order_by('-lokalizacja')
        request.session['lokalizacja_filter'] = 1

    print(queryset)
    context = {
    'queryset':queryset
    }
    return render(request,'projekt/filters/oferta/oferta_list_filter_lokalizacja.html',context)

def oferta_list_filter_wynagrodzenie(request):
    if(request.session['wynagrodzenie_filter'] ==1):
        queryset = Oferta.objects.all().order_by('wynagrodzenie')
        request.session['wynagrodzenie_filter'] = -1
    else:
        queryset=Oferta.objects.all().order_by('-wynagrodzenie')
        request.session['wynagrodzenie_filter'] = 1

    print(queryset)
    context = {
    'queryset':queryset
    }
    return render(request,'projekt/filters/oferta/oferta_list_filter_wynagrodzenie.html',context)


def aplikant_detail(request, pk):
    aplikant = get_object_or_404(Aplikant, pk=pk)
    return render(request, 'projekt/aplikant_detail.html', {'aplikant': aplikant})

def register_success(request):
    return render(request,'projekt/register_success.html')

def upload_success(request):
    return render(request,'projekt/upload_success.html')

def aplication_success(request):
    return render(request,'projekt/aplication_success.html')

class Register(View):
    template_name = 'projekt/form-login-register.html'


    def get(self, request):
        form = UserRegisterForm(None)
        return render(request, self.template_name,{'form': form})

    def post(self, request):
            form = UserRegisterForm(request.POST)

            print("Wartosc:", request.POST.get('inputs'))
            request.session['input'] = request.POST.get('inputs')

            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 and password2 and password1 != password2:
                    raise ("Password doesnt match.")

                user.set_password(password1)
                user.save()

                user = authenticate(username=username, password=password1)
                request.session['active_user_pk'] = User.objects.get(username=username).pk
                request.session['username'] = username
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.session['is_aplikant'] = is_aplikant(request.session['active_user_pk'])

                        return redirect('account_update', pk=request.session['active_user_pk'])
            return render(request, self.template_name, {'form': form})

def login_view(request):
    title = "Login"

    form = UserLoginForm(request.POST or None)

    print("Wartosc:", request.POST.get('inputs'))
    request.session['input'] = request.POST.get('inputs')

    if  form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        request.session['username'] = username
        request.session['active_user_pk'] = User.objects.get(username=username).pk ## Do Obsłużenia, wartosc null podczas powrotu ze strony admin!

        request.session['is_aplikant'] = is_aplikant(request.session['active_user_pk'])

        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect("account_update", pk=request.session['active_user_pk'])
    return render(request, "projekt/form-login-register.html",{"form":form, "title":title})

def logout_view(request):
    logout(request)
    return render(request, "projekt/logout.html",{})


def settings(request):
    try:
        object = Aplikant.objects.get(id=request.session['object_id'])
    except (KeyError, Aplikant.DoesNotExist):
        object = None
    return render(request, 'projekt/settings.html', {'object':object})


@login_required()
def edit_user(request, pk):
    if request.session['input'] == 'aplikant':
        user = User.objects.get(pk=pk)

        user_form = UserProfileForm(instance=user)

        ProfileInlineFormset = inlineformset_factory(User, Aplikant,
                                                     fields=('imie','wiek','wyksztalcenie','telefon','miasto',
                                                             'panstwo','opis'), max_num=1,extra=1)
        formset = ProfileInlineFormset(instance=user)

        if request.user.is_authenticated() and request.user.id == user.id:
            if request.method == "POST":
                user_form = UserProfileForm(request.POST, request.FILES, instance=user)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

                if user_form.is_valid():
                    created_user = user_form.save(commit=False)
                    formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                    if formset.is_valid():
                        created_user.save()
                        formset.save()
                        request.session['is_aplikant'] = is_aplikant(request.session['active_user_pk'])
                        return redirect('/aplikant/')

            return render(request, "projekt/account_update.html", {
                "noodle_form": user_form,
                "formset": formset,
            })
        else:
            raise PermissionDenied
    else:
        user = User.objects.get(pk=pk)

        user_form = UserProfileForm(instance=user)

        ProfileInlineFormset = inlineformset_factory(User, Firma,
                                                     fields=('nazwa_firmy', 'miasto', 'ulica', 'telefon', 'email'
                                                             ), max_num=1, extra=1)
        formset = ProfileInlineFormset(instance=user)

        if request.user.is_authenticated() and request.user.id == user.id:
            if request.method == "POST":
                user_form = UserProfileForm(request.POST, request.FILES, instance=user)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

                if user_form.is_valid():
                    created_user = user_form.save(commit=False)
                    formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                    if formset.is_valid():
                        created_user.save()
                        formset.save()
                        return redirect('/firma/')

            return render(request, "projekt/account_update.html", {
                "noodle_form": user_form,
                "formset": formset,
            })
        else:
            raise PermissionDenied

@login_required
def add_oferta(request):
    if request.session['input'] == 'firma':
        title = "Dodaj Oferte"
        form = OfertaForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('edit_oferts',request.session['active_user_pk'])

    return render(request, "projekt/form.html", {"form": form, "title": title})

@login_required
def edit_oferts(request,pk):
    if request.session['input'] == 'firma':

        title = "Twoje Oferty"
        user = User.objects.get(pk=pk)
        user_form = UserProfileForm(instance=user)

        OfertaInlineFormset = inlineformset_factory(User,Oferta,form=OfertaForm,extra=0)

        formset = OfertaInlineFormset(instance=user)

        if request.user.is_authenticated():
            if request.method == "POST":
                user_form = UserProfileForm(request.POST, request.FILES, instance=user)
                formset = OfertaInlineFormset(request.POST, request.FILES, instance=user)

                if user_form.is_valid():
                    created_user = user_form.save(commit=False)
                    formset = OfertaInlineFormset(request.POST, request.FILES, instance=created_user)

                    if formset.is_valid():
                        created_user.save()
                        formset.save()

            return render(request, "projekt/form_add_job.html", {"formset": formset, "title": title})

def upload_cv(request):
    instance = get_object_or_404(Aplikant, user_id=request.user.id)
    form = CvForm(request.POST or None,request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('upload_success')
    form = CvForm()
    return render(request, 'projekt/cv-form.html', {'form': form, 'instance':instance} )

def is_aplikant(user_pk):
    if Aplikant.objects.filter(user_id=user_pk).count() != 0:
        return 1
    else:
        return 0

def add_aplication(request):

    if(Aplikacja.objects.filter(user_id = request.user.id, oferta_id = request.session['active_oferta_id']).count()==0):
        user_oferta_owner_id = Oferta.objects.get(id=request.session['active_oferta_id']).user_id
        Aplikacja.objects.create(user_id = request.user.id,
                                 oferta_id = request.session['active_oferta_id'],
                                 user_oferta_owner_id = user_oferta_owner_id)
    else:
        print("Juz istnieje taka aplikacja")

    return render(request, 'projekt/aplication_success.html')

def show_aplications(request):
    title='Złożone CV'
    instances = []
    aplikacje = Aplikacja.objects.filter(user_oferta_owner_id = request.user.pk)
    for a in aplikacje:
        wakat = Oferta.objects.get(pk=a.oferta_id).wakat

        instances.append(
            {'cvk':Aplikant.objects.get(user_id = a.user_id),
             'wakat':wakat
             })

    return  render(request, 'projekt/aplications-list.html',{'instances':instances,'title':title})

def accept_aplication(request):

    return  render(request, 'projekt/aplications-list.html',{})

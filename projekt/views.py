from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.forms.models import inlineformset_factory, modelform_factory
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from os.path import join
from django.conf import settings

from .models import Firma, Oferta, Aplikant, Aplikacja
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout,get_user_model
from  django.views import generic
from django.views.generic import View
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, OfertaForm,UploadFileForm, CvForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.core.files.uploadedfile import SimpleUploadedFile




def oferta_list(request):
    oferta = Oferta.objects.filter(data_utworzenia__lte=timezone.now()).order_by('data_utworzenia')
    request.session['is_aplikant_cv']=0

    if request.user.is_authenticated():
        if(request.session['is_aplikant'] and Aplikant.objects.get(user_id=request.session['active_user_pk']).cv ): #User jest zalogowany jako aplikant i ma załadowane CV.
            print("MA CV")
            request.session['is_aplikant_cv']=1
    return render(request, 'projekt/oferta_list.html', {'oferta': oferta})

def oferta_detail(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    request.session['active_oferta_id'] = pk
    return render(request, 'projekt/oferta_detail.html', {'oferta': oferta})

def firma_list(request):
    firma = Firma.objects.all().order_by('nazwa_firmy')
    return render(request, 'projekt/firma_list.html', {'firma': firma})

def aplikant_list(request):
    request.session['wiek_filter'] = 1
    request.session['imie_filter'] = 1
    request.session['wyksztalcenie_filter'] = 1
    queryset = Aplikant.objects.all()
    print(queryset)
    context ={
        "queryset":queryset
    }
    return render(request, 'projekt/aplikant_list.html', context)

def aplikant_list_filter_wiek(request):
    #aplikant = Aplikant.objects.all().select_related('user').order_by('wiek') # Filtrowanie wzgledem wieku

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

def aplikant_detail(request, pk):
    aplikant = get_object_or_404(Aplikant, pk=pk)
    return render(request, 'projekt/aplikant_detail.html', {'aplikant': aplikant})

def register_success(request):
    return render(request,'projekt/register_success.html')

class Register(View):
    template_name = 'projekt/registration_form.html'


    # display blank form
    def get(self, request):
        form = UserRegisterForm(None)
        return render(request, self.template_name,{'form': form})

    def post(self, request):
            form = UserRegisterForm(request.POST)

            print("Wartosc:", request.POST.get('inputs'))
            request.session['input'] = request.POST.get('inputs')

            ##Zrobic walidację adresow email
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
        #try:
        #    object = Aplikant.objects.get(id=request.session['object_id'])
        #except (KeyError, Aplikant.DoesNotExist):
        #    object = None
        request.session['username'] = username
        request.session['active_user_pk'] = User.objects.get(username=username).pk ## Do Obsłużenia, wartosc null podczas powrotu ze strony admin!

        request.session['is_aplikant'] = is_aplikant(request.session['active_user_pk'])

        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect("account_update", pk=request.session['active_user_pk'])
    return render(request, "projekt/form.html",{"form":form, "title":title})

def logout_view(request):
    logout(request)
    return render(request, "projekt/form.html",{})


def settings(request):
    try:
        object = Aplikant.objects.get(id=request.session['object_id'])
    except (KeyError, Aplikant.DoesNotExist):
        object = None
    return render(request, 'projekt/settings.html', {'object':object})


@login_required()  # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    if request.session['input'] == 'aplikant':
        user = User.objects.get(pk=pk)

        # prepopulate UserProfileForm with retrieved user values from above.
        user_form = UserProfileForm(instance=user)

        # The sorcery begins from here, see explanation below

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
                "noodle": pk,
                "noodle_form": user_form,
                "formset": formset,
            })
        else:
            raise PermissionDenied
    else:
        user = User.objects.get(pk=pk)

        # prepopulate UserProfileForm with retrieved user values from above.
        user_form = UserProfileForm(instance=user)

        # The sorcery begins from here, see explanation below

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
                "noodle": pk,
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
            #return request, "projekt/"
    return render(request, "projekt/form.html", {"form": form, "title": title})

@login_required
def edit_oferts(request,pk):
    if request.session['input'] == 'firma':
        title = "Twoje Oferty"
        user = User.objects.get(pk=pk)
        print (user)
        user_form = UserProfileForm(instance=user)

        OfertaInlineFormset = inlineformset_factory(User,Oferta,form=OfertaForm,extra=0)
        #OfertaFormset = modelform_factory(Oferta,form=OfertaForm)

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
        return redirect('register_success')
    form = CvForm()
    return render(request, 'projekt/cv-form.html', {
    'form': form, 'instance':instance
})

def is_aplikant(user_pk):
    if Aplikant.objects.filter(user_id=user_pk).count() != 0:
        return 1
    else:
        return 0

def add_aplication(request):

    if(Aplikacja.objects.filter(user_id = request.user.id, oferta_id = request.session['active_oferta_id']).count()==0):
        user_oferta_owner_id = Oferta.objects.get(id=request.session['active_oferta_id']).user_id
        print('User_oferta_owner_id:')
        print(user_oferta_owner_id)
        Aplikacja.objects.create(user_id = request.user.id,
                                 oferta_id = request.session['active_oferta_id'],
                                 user_oferta_owner_id = user_oferta_owner_id)
    else:
        print("Juz istnieje")

    return render(request, 'projekt/register_success.html')

def show_aplications(request):
    title='Złożone CV'
    instances = []
    aplikacje = Aplikacja.objects.filter(user_oferta_owner_id = request.user.pk)
    for a in aplikacje:
        wakat = Oferta.objects.get(pk=a.oferta_id).wakat
        instances.append({'cvk':Aplikant.objects.get(user_id = a.user_id),'wakat':wakat})
    return  render(request, 'projekt/aplications-list.html',{'instances':instances,'title':title})

#DODAĆ SPRAWDZENIE CZY JEST ADMINEM. ZEBY NIE BYLO BLEDU PODCZAS PRZEJSCIA Z PANELU ADMNA DO APLIKACJI.
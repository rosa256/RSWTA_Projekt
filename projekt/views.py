from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from .models import Firma, Oferta, UserAplication
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout,get_user_model
from  django.views import generic
from django.views.generic import View
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
    aplikant = UserAplication.objects.all()
    return render(request, 'projekt/aplikant_list.html', {'aplikant': aplikant})

def firma_detail(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    return render(request, 'projekt/firma_detail.html', {'firma': firma})

def aplikant_detail(request, pk):
    aplikant = get_object_or_404(UserAplication, pk=pk)
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

            ##Zrobic walidację adresow email
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)
                request.session['active_user_pk'] = User.objects.get(username=username).pk
                request.session['username'] = username
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('account_update', pk=request.session['active_user_pk'])

            return render(request, self.template_name, {'form': form})

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)

    if  form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        #try:
        #    object = Aplikant.objects.get(id=request.session['object_id'])
        #except (KeyError, Aplikant.DoesNotExist):
        #    object = None
        request.session['username'] = username
        request.session['active_user_pk'] = User.objects.get(username=username).pk

        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect("account_update", pk=request.session['active_user_pk'])
    return render(request, "projekt/form.html",{"form":form, "title":title})

def logout_view(request):
    logout(request)
    return render(request, "projekt/form.html",{})


def settings(request):
    try:
        object = UserAplication.objects.get(id=request.session['object_id'])
    except (KeyError, UserAplication.DoesNotExist):
        object = None
    return render(request, 'projekt/settings.html', {'object':object})


@login_required()  # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserProfileForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserAplication,
                                                 fields=('imie','wiek','wyksztalcenie','pochodzenie','telefon','miasto',
                                                         'panstwo','opis'))
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
                    return redirect('/aplikant/')

        return render(request, "projekt/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
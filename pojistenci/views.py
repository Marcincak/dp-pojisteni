from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from .models import Pojistenec, Pojisteni, Uzivatel
from .forms import PojistenecForm, PojisteniForm, LoginForm, UzivatelForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class PojistenecIndex(LoginRequiredMixin, generic.ListView):
    model = Pojistenec
    template_name = "pojistenci/pojistenec_index.html"  # cesta k šabloně ze složky templates (je možné sdílet mezi aplikacemi)
    context_object_name = "seznam_pojistencu"  # pod tímto jménem budeme volat seznam objektů v šabloně
    paginate_by = 10

    # tato metoda nám získává seznam Pojistenu seřazených od největšího id (9,8,7...)
    def get_queryset(self):
        return Pojistenec.objects.all().order_by("-id")

class PojistenecSearch(LoginRequiredMixin, generic.ListView):
    model = Pojistenec
    template_name = "pojistenci/search_pojistenec.html"  # cesta k šabloně ze složky templates (je možné sdílet mezi aplikacemi)
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        queryset = Pojistenec.objects.all()
        if q:
            queryset = queryset.filter(
                Q(jmeno__icontains=q) | Q(prijmeni__icontains=q)
            )
        return queryset

    # tato metoda nám získává seznam nalezených Pojistenu
    def get_context_data(self, **kwargs):
        # přidáme query do kontextu, aby se zobrazilo zpět v inputu
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class CurrentPojistenec(generic.DetailView):

    model = Pojistenec
    template_name = "pojistenci/pojistenec_detail.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")
        try:
            pojistenec = self.get_object()
            pojisteni_seznam = pojistenec.pojisteni_set.all().order_by("-id")
        except:
            return redirect("pojistenec_index")
        return render(request, self.template_name, {
            "pojistenec": pojistenec,
            "pojisteni_seznam": pojisteni_seznam
        })

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_pojistenec", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání pojištěnce.")
                    return redirect("pojistenec_index")
                else:
                    self.get_object().delete()
                    messages.info(request, "Pojištěnec byl smazán.")
        return redirect("pojistenec_index")

class CreatePojistenec(LoginRequiredMixin, generic.edit.CreateView):

    form_class = PojistenecForm
    template_name = "pojistenci/vytvor_pojistenec.html"

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištěnce.")
            return redirect("pojistenec_index")
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    # Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří noveho pojistence; pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištěnce.")
            return redirect("pojistenec_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request, "Pojištěnce byl přidán.")
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"form": form})



class PojisteniIndex(LoginRequiredMixin, generic.ListView):

    template_name = "pojistenci/pojisteni_index.html"  # cesta k šabloně ze složky templates (je možné sdílet mezi aplikacemi)
    context_object_name = "seznam_pojisteni"  # pod tímto jménem budeme volat seznam objektů v šabloně
    paginate_by = 10

    # tato metoda nám získává seznam Pojisteni seřazených od největšího id (9,8,7...)
    def get_queryset(self):
        return Pojisteni.objects.all().order_by("-id")


class CurrentPojisteni(generic.DetailView):

    model = Pojisteni
    template_name = "pojistenci/pojisteni_detail.html"

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        pojisteni = self.get_object()  # Získání pojištění hned na začátku

        if request.user.is_admin:
            if "edit" in request.POST:
                return redirect("edit_pojisteni", pk=pojisteni.pk)
            else:
                pojistenec_pk = pojisteni.pojistenec.pk  # Získání ID pojistence
                pojisteni.delete()
                messages.info(request, "Pojištění bylo smazáno.")
                return redirect('pojistenec_detail', pk=pojistenec_pk)

        messages.info(request, "Nemáš práva pro smazání pojištění.")
        return redirect("pojisteni_index")



class CreatePojisteni(generic.edit.CreateView):

    form_class = PojisteniForm
    template_name = "pojistenci/vytvor_pojisteni.html"

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro vytvoření noveho pojištění.")
            return redirect("pojistenec_index")
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})


    # Metoda pro POST request, zkontroluje formulář; pokud je validní, vytvoří nove pojisteni; pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        form = self.form_class(request.POST)
        if form.is_valid():
            pojisteni = form.save(commit=True)
            messages.info(request, "Pojištění bylo přidáno.")
            return redirect('pojistenec_detail', pk=pojisteni.pojistenec.pk)
        return render(request, self.template_name, {"form": form})

class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "pojistenci/user_form.html"

    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro registraci noveho uživatele.")
            return redirect("pojistenec_index")
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro registraci noveho uživatele.")
            return redirect("pojistenec_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit=False)
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"form": form})

class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "pojistenci/login_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlášit znovu.")
            return redirect("pojistenec_index")
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlášit znovu.")
            return redirect("pojistenec_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("pojistenec_index")
            else:
                messages.error(request, "Tento účet neexistuje nebo bylo zadáno nesprávné heslo.")
        return render(request, self.template_name, {"form": form})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
    return redirect("login")


class EditPojistenec(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = "pojistenci/vytvor_pojistenec.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištěnce.")
            return redirect("pojistenec_index")
        try:
            pojistenec = Pojistenec.objects.get(pk=pk)
        except:
            messages.error(request, "Tento pojistenec neexistuje!")
            return redirect("pojistenec_index")
        form = self.form_class(instance=pojistenec)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištěnce.")
            return redirect("pojistenec_index")
        form = self.form_class(request.POST)

        if form.is_valid():
            jmeno = form.cleaned_data["jmeno"]
            prijmeni = form.cleaned_data["prijmeni"]
            email = form.cleaned_data["email"]
            telefon = form.cleaned_data["telefon"]
            ulice = form.cleaned_data["ulice"]
            cislo = form.cleaned_data["cislo"]
            mesto = form.cleaned_data["mesto"]
            psc = form.cleaned_data["psc"]
            try:
                pojistenec = Pojistenec.objects.get(pk=pk)
            except:
                messages.error(request, "Tento pojištěnce neexistuje!")
                return redirect("pojistenec_index")
            pojistenec.jmeno = jmeno
            pojistenec.prijmeni = prijmeni
            pojistenec.email = email
            pojistenec.telefon = telefon
            pojistenec.ulice = ulice
            pojistenec.cislo = cislo
            pojistenec.mesto = mesto
            pojistenec.psc = psc
            pojistenec.save()
            messages.info(request, "Pojištěnec byl změněn.")
            return redirect("pojistenec_detail", pk=pojistenec.id)
        return render(request, self.template_name, {"form": form})

class EditPojisteni(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojisteniForm
    template_name = "pojistenci/vytvor_pojisteni.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištění.")
            return redirect("pojisteni_index")
        try:
            pojisteni = Pojisteni.objects.get(pk=pk)
        except:
            messages.error(request, "Toto pojištění neexistuje!")
            return redirect("pojisteni_index")
        form = self.form_class(instance=pojisteni)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.info(request, "Musíš se nejdříve přihlášit.")
            return redirect("login")

        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištění.")
            return redirect("pojisteni_index")
        form = self.form_class(request.POST)

        if form.is_valid():
            pojistenec = form.cleaned_data["pojistenec"]
            typ = form.cleaned_data["typ"]
            castka = form.cleaned_data["castka"]
            predmet_pojisteni = form.cleaned_data["predmet_pojisteni"]
            platnost_od = form.cleaned_data["platnost_od"]
            platnost_do = form.cleaned_data["platnost_do"]
            try:
                pojisteni = Pojisteni.objects.get(pk=pk)
            except:
                messages.error(request, "Toto pojištění neexistuje!")
                return redirect("pojisteni_index")
            pojisteni.pojistenec = pojistenec
            pojisteni.typ = typ
            pojisteni.castka = castka
            pojisteni.predmet_pojisteni = predmet_pojisteni
            pojisteni.platnost_od  = platnost_od
            pojisteni.platnost_do = platnost_do
            pojisteni.save()
            messages.info(request, "Pojištění bylo změněno.")
            return redirect('pojistenec_detail', pk=pojisteni.pojistenec.pk)
        return render(request, self.template_name, {"form": form})
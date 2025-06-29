from django import forms
from .models import Pojistenec, Pojisteni, Uzivatel


class PojistenecForm(forms.ModelForm):
    class Meta:
        model = Pojistenec
        fields = '__all__'

    # Nepovinné – můžeš přidat čistící metody navíc, pokud chceš třeba odstranit extra mezery apod.
    def clean_jmeno(self):
        jmeno = self.cleaned_data['jmeno'].strip()
        return jmeno

    def clean_prijmeni(self):
        prijmeni = self.cleaned_data['prijmeni'].strip()
        return prijmeni

    def clean_mesto(self):
        mesto = self.cleaned_data['mesto'].strip()
        return mesto









class PojisteniForm(forms.ModelForm):

    class Meta:
        model = Pojisteni
        fields = ["pojistenec", "typ", "castka", "predmet_pojisteni", "platnost_od", "platnost_do"]
        error_messages = {
            'platnost_od': {
                'invalid': "Neplatný formát data. Použijte RRRR-MM-DD, například 2025-06-29.",
            },
            'platnost_do': {
                'invalid': "Neplatný formát data. Použijte RRRR-MM-DD, například 2025-06-29.",
            }
        }


class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ["email", "password"]

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ["email", "password"]
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator

# Validátory
text_validator = RegexValidator(
    regex=r'^[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž\s-]+$',
    message='Pole smí obsahovat pouze písmena, mezery nebo pomlčky.'
)

min_length_validator = MinLengthValidator(
    2,
    message='Pole musí mít alespoň 2 znaky.'
)

max_length_validator = MaxLengthValidator(
    100,
    message='Pole může mít maximálně 100 znaků.'
)

telefon_validator = RegexValidator(
    regex=r'^\+?[\d\s]{9,20}$',
    message='Zadejte platné telefonní číslo.'
)

psc_validator = RegexValidator(
    regex=r'^\d{3}\s?\d{2}$',
    message='Zadejte platné PSČ ve formátu 12345 nebo 123 45.'
)

alphanum_space_dash_validator = RegexValidator(
    regex=r'^[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž0-9\s-]+$',
    message='Pole smí obsahovat pouze písmena, čísla, mezery nebo pomlčky.'
)

castka_min_validator = MinValueValidator(
    1,
    message="Částka musí být alespoň 1 Kč."
)

castka_max_validator = MaxValueValidator(
    100000000,
    message="Částka nesmí přesáhnout 100 000 000 Kč."
)

class Pojistenec(models.Model):
    jmeno = models.CharField(max_length=100, validators=[text_validator, min_length_validator, max_length_validator])
    prijmeni = models.CharField(max_length=100, validators=[text_validator, min_length_validator, max_length_validator])
    email = models.EmailField(max_length=100, validators=[EmailValidator(), max_length_validator])
    telefon = models.CharField(max_length=22, validators=[telefon_validator])
    ulice = models.CharField(max_length=100, validators=[alphanum_space_dash_validator, min_length_validator, max_length_validator])
    cislo = models.CharField(max_length=100, validators=[alphanum_space_dash_validator, max_length_validator])
    mesto = models.CharField(max_length=100, validators=[alphanum_space_dash_validator, min_length_validator, max_length_validator])
    psc = models.CharField(max_length=6, validators=[psc_validator])

    def __str__(self):
        return "Jméno: {0} | Příjmení: {1} | Email: {2}".format(self.jmeno, self.prijmeni, self.email)

    class Meta:
        verbose_name = "Pojištěnec"
        verbose_name_plural = "Pojištěnci"


class Pojisteni(models.Model):
    pojistenec = models.ForeignKey(Pojistenec, on_delete=models.CASCADE)
    typ = models.CharField(max_length=100, validators=[alphanum_space_dash_validator, min_length_validator, max_length_validator])
    castka = models.IntegerField(validators=[castka_min_validator, castka_max_validator])
    predmet_pojisteni = models.CharField(max_length=100, validators=[alphanum_space_dash_validator, min_length_validator, max_length_validator])
    platnost_od = models.DateField()
    platnost_do = models.DateField()

    def __str__(self):
        return "Pojištěnec: {0} | Předmět pojistení: {1}".format(self.pojistenec, self.predmet_pojisteni)

    class Meta:
        verbose_name = "Pojištění"
        verbose_name_plural = "Pojištění"



class UzivatelManager(BaseUserManager):
    # Vytvoří uživatele
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
            return user
    # Vytvoří admina
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user

class Uzivatel(AbstractBaseUser):

    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    objects = UzivatelManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "email: {}".format(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
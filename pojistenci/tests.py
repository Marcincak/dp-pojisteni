from django.test import TestCase
from django.urls import reverse  # pro test našeho "filmovy_index" view

from .models import Pojistenec, Pojisteni, Uzivatel  # pro test modelu


class PojistenecTestCase(TestCase):
    def setUp(self):
        self.name = Pojistenec.objects.create(jmeno="Test Jmeno")
        self.prijmeni = Pojistenec.objects.create(prijmeni="Test prijmeni")
        self.email = Pojistenec.objects.create(email="Test email")


    def test_create_pojistenec(self):
        ocekavany_jmeno = "Test Jmeno"
        ocekavana_prijmeni = "Test prijmeni"
        ocekavany_email = "Test email"


        pojistenec = Pojistenec.objects.create(
            jmeno=ocekavany_jmeno,
            prijmeni=ocekavana_prijmeni,
            email=ocekavany_email,
        )
        self.assertEqual(pojistenec.jmeno, ocekavany_jmeno)
        self.assertEqual(pojistenec.prijmeni, ocekavana_prijmeni)
        self.assertEqual(pojistenec.email, ocekavany_email)


    def test_pojistenec_str_representation(self):
        pojistenec = Pojistenec.objects.create(
            jmeno="Test Jmeno",
            prijmeni="Test Prijmeni",
            email="Test Email",
        )

        ocekavany_str = (
            "Jméno: Test Jmeno | Příjmení: Test Prijmeni | Email: Test Email"
        )
        self.assertEqual(str(pojistenec), ocekavany_str)

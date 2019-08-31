from ..views import get_alternatives, check_products, calc_full_price
from spellchecker import SpellChecker
from django.utils import timezone
from django.test import TestCase
from ..models import Grocery_List
from colorama import Fore, init
import os

init(autoreset=True)

# Create your tests here.
class ProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.banana = Grocery_List.objects.create(title="EDEKA Bananen", quantity="2",\
        date=timezone.now(), unit="1 Stück",search="Bananen",price="0.40")

        cls.sauce = Grocery_List.objects.create(title="﻿Appel Worcester Sauce",\
        date=timezone.now(), quantity="1", unit="400ml",search="Worcester Sauce", \
        price="1.69")


    def setUp(self):
        self.banana.refresh_from_db()
        self.sauce.refresh_from_db()


    def test_get_alternatives_banana(self):
        self.assertEqual(get_alternatives(self.banana),\
        [[0, 'EDEKA Bananen', '0.40', '1 Stück'], \
        [1, 'EDEKA Bio Bananen', '0.30', '1 Stück'], \
        [2, 'Bio Alnatura Bananen Chips', '1.19', '150g'], \
        [3, 'Bio Zentrale Bananen Chips', '1.79', '150g'], \
        [4, 'Bio Hipp Früchte Äpfel mit Bananen nach dem 4.Monat', '0.95', '190g'], \
        [5, 'Bio Hipp Frucht&Getreide Mango Bananen Grieß ab dem 6.Monat', '0.95', '190g'], \
        [6, 'Bebivita Bananen Früchtesaft nach dem 4.Monat', '0.75', '0,5l'], \
        [7, 'Kubus Karotten Apfel Bananen Saft', '1.79', '900ml']], \
        Fore.RED + "\nDid not get correct alternatives for EDEKA Bananen.")
        print(Fore.GREEN + "\nGot correct alternatives for EDEKA Bananen.")


    def test_get_alternatives_sauce(self):
        self.assertEqual(get_alternatives(self.sauce), [[0, 'Appel Worcester Sauce', '1.69', '140ml'], \
        [1, 'Bio Zentrale Worcestershire Sauce', '2.99', '140ml'], \
        [2, 'Kattus Worcester Sauce', '2.29', '140ml']], Fore.RED + "\nDid not get correct alternatives \
        for Appel Worcester Sauce.")
        print(Fore.GREEN + "\nGot correct alternatives for Appel Worcester Sauce.")


    def test_get_banana(self):
        self.assertEqual(check_products(self.banana.search), ['EDEKA Bananen', '0.40', '1 Stück'], \
        Fore.RED + "Did not get correct product.")
        print(Fore.GREEN + "\nGot correct product.")


    def test_get_sauce(self):
        self.assertEqual(check_products(self.sauce.search), ['Appel Worcester Sauce', '1.69', '140ml'], \
        Fore.RED + "Did not get correct product.")
        print(Fore.GREEN + "\nGot correct product.")

    def test_calc_full_price(self):
        full_price = calc_full_price()
        self.assertEqual(full_price, 2.49, Fore.RED + "\ncalc_full_price returned\
        a wrong value! \nExpected: 2.49\nGot: "+str(full_price))
        print(Fore.GREEN+"\n calc_full_price returned the right price.")

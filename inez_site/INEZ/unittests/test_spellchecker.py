from ..views import capitaliziation, spellcheck
from django.test import TestCase
from colorama import Fore, init
import os

init(autoreset=True)

class SpellCheckerTest(TestCase):


    #    def setUp(self):
    #        self.spellchecker = SpellChecker(local_dictionary=os.getcwd() + "\\INEZ\\static\\INEZ\\json\\spellings.json", case_sensitive=True)


        def test_capitalization(self):
            caps = capitaliziation("capitalize every word")
            self.assertEqual(caps, "Capitalize Every Word", \
            Fore.RED + "Expected: 'Capitalize Every Word'\n Got: " + caps)
            print(Fore.GREEN+"\n capitaliziation() returned correct string.")


        def test_spellchecker_single(self):
            self.assertEqual("Butter", spellcheck("Buter"))
            print(Fore.GREEN+"\n Corrected 'Buter' to 'Butter'.")
            self.assertEqual("Kartoffel", spellcheck("Karrtofel"))
            print(Fore.GREEN+"\n Corrected 'Karrtofel' to 'Kartoffel'.")
            self.assertEqual("Milch", spellcheck("Milhc"))
            print(Fore.GREEN+"\n Corrected 'Milhc' to 'Milch'.")


        def test_spellchecker_multiple(self):
            self.assertEqual("Kerrygold Butter", spellcheck("Kerygold Buttr"))
            print(Fore.GREEN+"\n Corrected 'Kerygold Buttr' to 'Kerrygold Butter'.")
            self.assertEqual("Salat Kartoffel Mayo",spellcheck("Salad Katoffle Majo"))
            print(Fore.GREEN+"\n Corrected 'Salad Katoffle Majo' to 'Salat Kartoffel Mayo'.")
            self.assertEqual("Landliebe Milch", spellcheck("Lanlibe Milhc"))
            print(Fore.GREEN+"\n Corrected 'Lanlibe Milhc' to 'Landliebe Milch'.")

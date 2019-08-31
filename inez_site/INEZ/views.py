from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from spellchecker import SpellChecker
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Grocery_List
from colorama import init, Fore
from operator import itemgetter
import numpy as np
import logging
import math
import os
import re

# ______INITIALIZATIONS________
init(autoreset=True)    # Colorama for printing colored text in the terminal
dirpath = os.getcwd()   # path of the project
spellchecker = SpellChecker(local_dictionary=dirpath + \
"\\INEZ\\static\\INEZ\\json\\spellings.json", case_sensitive=True) #Spellchecker

# loading the ~14000 products from cache if possible, else loading them from
# file and caching them
if cache.get("products") is not None:
    products = cache.get("products")
else:
    products = {}
    with open(os.getcwd()+"\\INEZ\\products.txt", encoding="utf-8-sig") as f:
        for line in f:
            values = line.split("|")
            products[values[0]] = [values[1].replace(",","."), values[2].replace("\n","")]
    print(Fore.GREEN + 'Loaded %s products\n' % len(products))
    cache.set("products", products, (60*60))

logger = logging.getLogger(__name__) # Initializing logger


def get_alternatives(item):
    """
    Getting all alternatives for the item passed to the function.
    """
    title = item.search
    # if the search term consists of multiple words, match only items containing ALL
    # of these words
    # Example:
    # item.search equals "Kerrygold Butter" -> function should not return
    # "Kerrygold Cheddar" or "Landliebe Butter"
    if len(title.split(" ")) >= 2:
        words = title.split(" ")

        prod = []
        for part in words:
            for key, value in products.items():
                if part.lower() in key.lower():
                    prod.append(key)


        seen = set()
        doubles = []
        for x in prod:
            if x in seen:
                doubles.append(x)
            seen.add(x)

        items = []
        prods = []
        for item in doubles:
            for key, value in products.items():
                if item.lower() in key.lower():
                    prods.append([key,value])
                    break;
        i = 0

        # format products to match [index, title, price, unit]
        for prod in prods:
            alt_list = [i, prod[0], prod[1][0], prod[1][1]]
            items.append(alt_list)
            i+=1
        return items

    # search term consists of only one word (e.g. "Butter")
    else:
        # Searching EXCLUSIVELY for the term used to find the item.
        # This does NOT match compound words.
        # Example: 'Butter' will not match 'Butterkäse'
        alternatives = [[key, value] for key, value in products.items() if item.search.lower() in key.lower().split(" ")]

        if alternatives != []:
            formatted = []
            i = 0

            for alt in alternatives:
                # Same formatting as above.
                # alt_list = [index, title, price, unit]
                # Example:
                # alt_list = [0, "Kerrygold Original Irische Butter", 2.39, "250g"]
                alt_list = [i, alt[0], alt[1][0], alt[1][1]]
                formatted.append(alt_list)
                i += 1
            return sorted(formatted, key=itemgetter(0))
        else:
            # Broader search for the term used to find the item.
            # This DOES match compound words.
            # Example: 'Butter' will match 'Butterkäse'
            alternatives = [[key,value] for key, value in products.items() if item.search.lower() in key.lower()]
            if alternatives != []:
            # Same procedure as above.
                formatted = []
                i = 0

                for alt in alternatives:
                    alt_list = [i, alt[0], alt[1][0], alt[1][1]]
                    formatted.append(alt_list)
                    i += 1
                return sorted(formatted, key=itemgetter(0))
            else:
                return []



def check_products(title):
    """
    A function for checking whether a requested item is sold at EDEKA.
    First tries to match the exact name, if that fails also considers compound
    words (example: no match for "Butter" -> returns "Butterkäse")
    """
    if len(title.split(" ")) >= 2:
        words = title.split(" ")

        prod = []
        for part in words:
            for key, value in products.items():
                if part.lower() in key.lower():
                    prod.append(key)

        seen = set()
        matching_items = []
        for x in prod:
            if x in seen:
                matching_items.append(x)
            seen.add(x)

        print("\nFound the following items matching " + Fore.CYAN + title + Fore.RESET + ":\n")

        for item in matching_items:
            print(item + "\n")

        item = []
        prods = [[key,value] for key, value in products.items() if matching_items[0] in key]
        prod = prods[0][1]
        item.append(prods[0][0])
        item.append(prod[0])
        item.append(prod[1])
        return item
    else:
        # Same as at get_alternatives, matches whole words
        titles = [[key,value] for key, value in products.items() if title.lower() in key.lower().split(" ")]
        print("\nFound the following items matching " + Fore.CYAN + title + Fore.RESET + ":\n")

        for title in titles:
            print(title)
            print("")
            if titles != []:
                title = []
                prod = titles[0][1]
                title.append(titles[0][0])
                title.append(prod[0])
                title.append(prod[1])
                return title #returning the first item which matches the search term
            else:
                print(Fore.YELLOW + "Did not find matching items, expanding search.")
                titles = [[key,value] for key, value in products.items() if title.lower() in key.lower()]
                if titles != []:
                    print(Fore.GREEN + "Match(es) found for " + Fore.RESET + title + Fore.GREEN + ":\n")

                    for ti in titles:
                        print(ti)

                    title = []
                    prod = titles[0][1]
                    title.append(titles[0][0])
                    title.append(prod[0])
                    title.append(prod[1])
                    return title
                else:
                    print(Fore.RED + "Did not find matching items! Adding custom item to list.")


def capitaliziation(title):
    """
    Capitalizes a list of words.
    """
    list = title.split(" ")
    title_new = []
    for part in list:
        title_new.append(part.capitalize())

    return " ".join(title_new)


def spellcheck(title):
    """
    Checks spelling of the title and corrects it if necessary.
    Works with a Levensthein-Distance of 2, meaning two wrong characters
    can be corrected.
    """
    title_old = capitaliziation(title)

    list = title.split(" ")
    for i in range(len(list)):
        if spellchecker.word_probability(list[i]) < 0.9:
            list[i] = spellchecker.correction(list[i]).capitalize()
            title_new = " ".join(list)

    if title_old != title_new:
        print("\nCorrected " + Fore.CYAN + title_old + Fore.RESET + " to " + Fore.CYAN + title_new)

    return title_new


def calc_full_price():
    """
    A function for calculating the sum of all prices on the grocery list
    """
    price = 0.0
    for item in Grocery_List.objects.all():
        price += item.price * item.quantity
    return price


def index(request):
    """
    Function that gets called whenever the 'add' or 'delete' buttons are pressed
    Processes the request and adds the item to the database or deletes the selected.
    """
    price = calc_full_price();
    items = Grocery_List.objects.all()

    if request.method == "POST":
        if "itemAdd" in request.POST:
            title = request.POST["title"]
            quantity = request.POST["quantity"]

            title = spellcheck(title)
            search = title
            product = check_products(title)

            # if there is no product matching the search, create a custom item
            if product != None:
                title = product[0]
                price = product[1]
                unit = product[2]
            else:
                price = 0.00
                unit = "unbekannt"


            logger.error(Fore.GREEN + "--------------------")
            logger.error(Fore.GREEN +"Product " + repr(title) + " costs " + str(price) + " per " + str(unit))
            logger.error(Fore.GREEN +"--------------------")

            # should the title be shorter than the 35 characters required
            # for a linebreak, add a linebreak and an invisible character to
            # ensure that the layout stays consistent
            if len(title) < 35:
                title += "\n "+u"⠀"

            # try to match the item to an item already existing on the list
            # should there be such an item, increase the quantity of the newly
            # added item by the quantity of the old item and delete the old item
            try:
               ex_item = Grocery_List.objects.get(title=title)
               if math.isclose(ex_item.price, float(price)):
                   quantity = ex_item.quantity + int(quantity)
                   ex_item.delete()
               else:
                   # should the title match, but different prices are supplied,
                   # ask the user tp rename their item
                   logger.error(Fore.RED +"Duplicate item name.")
                   messages.error(request, "Es gibt schon einen Artikel mit diesem Namen auf der Liste.\n Bitte wählen Sie einen anderen Namen.")
                   return redirect("/")
            except Grocery_List.DoesNotExist:
                logger.error(Fore.YELLOW +"Item " + title + " does not exist yet!\n")

            # create the item with the values generated in the previous steps
            # and add it to the list
            Item = Grocery_List(title=title, price=price.replace(",","."), quantity=quantity, unit=unit, date=timezone.now(), search=search)
            Item.save()
            messages.success(request, "Artikel erfolgreich hinzugefügt!")
            price = calc_full_price()
            return render(request,"index.html",{"items":items, "price":round(price,2)})
        elif "itemDelete" in request.POST:
            list = request.POST.getlist("checked")

            for item_id in list:
                item = Grocery_List.objects.get(id=int(item_id))
                item.delete()
            price = calc_full_price()

    return render(request,"index.html",{"items":items, "price":round(price,2)})

@csrf_protect
def item_alt(request, pk):
    """
    Function that gets called when the 'alternatives' button is pressed.
    Gathers all items with a similar name to the item on the list and
    display them in a modal for the user to choose from.
    """
    template_name = '../templates/item_alt_form.html'

    item = Grocery_List.objects.get(id=int(pk))
    items = get_alternatives(item)

    if request.method == 'POST':
        item_new = items[int(request.POST["id"])]
        print(item_new[1])

        # the following steps are pretty much identical to the steps taken in
        # the 'index' method.
        try:
           ex_item = Grocery_List.objects.get(title=item_new[1])
           print(ex_item.title)
           if math.isclose(ex_item.price, float(item_new[2])):
               ex_item.quantity += int(item.quantity)
               ex_item.save()
               item.delete()
           else:
               return redirect("/")
        except Grocery_List.DoesNotExist:
            title = item_new[1]

            if len(title) < 35:
                title += "\n "+u"⠀"

            item.title = title
            item.price = item_new[2]
            item.unit = item_new[3]
            item.save()

    return render(request, template_name, {
        'items': items
    })

def item_edit(request, pk):
    """
    Function tat gets called when the 'edit' button is pressed.
    Brings up a modal in which the user can edit key details of an item
    (title, price, quantity and unit)
    """
    template_name = '../templates/item_edit_form.html'

    item = Grocery_List.objects.get(id=int(pk))

    if request.method == 'POST':
        title = request.POST["title"]
        price = request.POST["price"]
        qty  = request.POST["quantity"]
        unit = request.POST["unit"]

        if len(title) < 35:
            title += "\n "+u"⠀"

        if price == "":
            price = item.price

        try:
           ex_item = Grocery_List.objects.get(title=title)
           if math.isclose(ex_item.price, float(price)) and (unit.lower() == ex_item.unit.lower()) and ex_item.id != item.id:
               ex_item.quantity += int(qty)
               ex_item.save()
               item.delete()
               return render(request, template_name, {'item':item})
        except Grocery_List.DoesNotExist:
            logger.warning(Fore.YELLOW + "Item did not exist.")


        if title != "":
            item.title = title
            item.search = title
        if price != "":
            item.price = price
        if unit != "":
            item.unit = unit
        if qty != "":
            item.quantity = qty
        item.save()
    else:
        pass
    return render(request, template_name, {'item':item})

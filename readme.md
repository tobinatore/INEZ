# INEZ - ein INtelligenter EinkaufsZettel
#### INGL - an INtelligent Grocery List

### Inhalt / Table of contents
[*DE*](#de) / [*EN*](#en)
#### DE
1. [Einleitung](#intro-de)
2. [Setup](#setup-de)
3. [Die Anwendung benutzen](#using-de)

#### EN
1. [Intro](#intro-en)
2. [Setup](#setup-en)
3. [Using the application](#using-en)

<a id="intro-de"></a>
### Einleitung
Eine Django Applikation, welche im Rahmen einer Coding Competition der IT-Talents GmbH in Partnerschaft mit der EDEKA DIGITAL GmbH entwickelt wurde. Die Aufgabe lautete:
> Für die Planung deines Wocheneinkaufs soll die intelligente Einkaufliste deinen Wunsch interpretieren und entsprechende Vorschläge machen.
Die Usability ist für den Anwender einfach zu halten. INEZ macht Vorschläge, korrigiert Eingaben und interpretiert die passenden Mengen.
So soll z.B. die Eingabe "1 Milch" zu "1 Liter Milch" angepasst werden.

Die Anwendung erfüllt die Aufgabe, indem Sie im Hintergrund eine Liste mit 14772 bei Edeka verkauften Produkten im Cache hält und nach einer Rechtschreibprüfung der Eingabe das passende Produkt auswählt.
Dabei wird darauf geachtet, dass nur die gesuchten Begriffe enthalten sind (so soll eine Anfrage nach "Kerrygold Butter" nicht "Landliebe Butter" zurückgeben) und dem Nutzer wird sowohl die Möglichkeit gegeben Alternativen auszuwählen, als auch das automatisch ausgewählte Produkt zu bearbeiten.

<a id="setup-de"></a>
### Setup
Das Projekt verwendet Pipenv für das Dependency Management. Bevor es also ausgeführt werden kann, muss zunächst Pipenv installiert werden.
Dies funktioniert ganz einfach über pip:

	pip install pipenv

Ist die Installation abgeschlossen, so muss in das Verzeichnis des Projektes navigiert werden, in welchem das pipfile und pipfile.lock liegen. Danach muss dann lediglich mittels `pipenv sync` das virtualenv erstellt und die Packages heruntergeladen werden.
Der Ablauf ist also wie folgt:

	C:\Windows\system32> cd C:\Users\User\Downloads\INEZ\INEZ
	C:\Users\User\Downloads\INEZ\INEZ> pipenv sync

Nachdem das virtualenv erstellt und die Packages heruntergeladen sind, kann mittels `pipenv shell` im selben Verzeichnis das virtualenv gestartet werden.
Da die Python Dateien noch ein Verzeichnis tiefer, in "inez_site" liegen, muss mittels `cd inez_site` nochmals das Verzeichnis gewechselt werden.
Dann kann man durch Verwendung von `python manage.py runserver` die Anwendung starten und mit `python manage.py test INEZ.unittests` die Unittests starten.

Der gesamte Ablauf von Installation bis Ausführung ist also:

	pip install pipenv
	cd C:\Users\User\Downloads\INEZ\INEZ
	pipenv sync
	pipenv shell
	cd inez_site
	python manage.py runserver

Die Seite ist mit jedem Browser unter 127.0.0.1:8000 erreichbar.
<a id="using-de"></a>
### Die Anwendung benutzen
Die Usability ist simpel gehalten. Neue Einträge können nach ausfüllen der Felder "Titel" und "Menge" durch einen Klick auf den Button "Zur Liste hinzufügen" angelegt werden und werden automatisch einer Rechtschreibprüfung (mit Levensthein-Distanz = 2, also 2 Fehler werden erkannt) unterzogen. INEZ füllt dann für den besten Match noch die Felder "Einheit" (z.B. 1l) und "Preis", und zeigt den vollen Titel (z.B. ergibt die Suche nach "Kerrygold Butter" "Kerrygold Original Irische Butter") und die vorher festgelegte Menge an.
Wenn man die Maus über einen Eintrag bewegt, wird das Feld "Bearbeiten" sichtbar. Durch einen Klick darauf wird ein Dialog geöffnet, indem man sämtliche Attribute des Produktes (Titel, Preis, Menge, Einheit) bearbeiten kann. Durch einen Klick auf "Speichern" werden die geänderten Werte übernommen.
Desweiteren gibt es unter dem angezeigten Preis einen Button "Alternativen". Dieser öffnet einen Dialog in dem man ein alternatives Produkt wählen kann, sollte die automatische Wahl nicht das richtige getroffen haben.
Löschen kann man Einträge, indem man die Checkbox neben dem Titel anklickt und auf den Button "Artikel löschen" klickt. Es können sowohl eines als auch mehrere Produkte gleichzeitig gelöscht werden.
Unter der Liste wird zudem jederzeit der Gesamtpreis des Einkaufs angezeigt. 
#### EN  

<a id="intro-en"></a>

### Intro  
A Django application which was developed for a coding competition hosted by IT-Talents GmbH and their partner EDEKA DIGITAL. 
The task was:
> For planning your weekly grocery shopping, the intelligent grocery list should interpret your wishes and suggest products.
Usability is to be kept simple. INGL suggests products, corrects input and interprets the quantities.
For example, an input of "1 milk" should be corrected to "1 litre milk".

The application solves that task by keeping a list of 14772 products sold at Edeka in the cache and returning the matching product after spellchecking the input.
It especially takes care of only returning products which have all searched terms in their title (e.g. searching for "Kerrygold Butter" should not return "Landliebe Butter"). Further than that the user has the possibility of selecting alternatives or outright editing the automatically selected item.

<a id="setup-en"></a>

### Setup  
This project uses pipenv as dependency management. Before you can run it you'll need to install pipenv and create the virtualenv.
The first step is easily done with pip:

	pip install pipenv

When the package finished installing, you'll have to navigate to the directory in which the pipfile and the pipfile.lock reside. After that the virtualenv containing the packages has to be created using `pipenv sync`.
So for example:

	C:\Windows\system32> cd C:\Users\User\Downloads\INEZ\INEZ
	C:\Users\User\Downloads\INEZ\INEZ> pipenv sync

After creating the virtualenv and downloading all packages, you can start the virtualenv using  `pipenv shell`.
Because of the structure of the directories, you need to change into the subdirectory "inez_site" with `cd inez_site`.
Finally you can start the server by typing `python manage.py runserver`. If you'd rather run the unittests,  `python manage.py test INEZ.unittests` is the command for that.

From installing to running:

	pip install pipenv
	cd C:\Users\User\Downloads\INEZ\INEZ
	pipenv sync
	pipenv shell
	cd inez_site
	python manage.py runserver

You can acces the site with any browser by typing 127.0.0.1:8000 into the adress bar.

<a id="using-en"></a>

### Using the application  
Usability is kept simple. New entries can be created by filling out the "Titel" and "Menge"(quantity) fields and are saved after clicking the "Zur Liste hinzufügen" ("add to list") button. Titles are getting spellchecked as soon as they are submitted. INGL will then add values to the fields "Einheit" (unit) (e.g. 1l) and "Preis" ("price") for the best match, and shows the full title (e.g. searching for "Kerrygold Butter" will yield "Kerrygold Original Irische Butter" as a result) and the previously specified quantity.
When moving the cursor over an entry, the button "Bearbeiten" (edit) will become visible. Clicking on that button opens a modal in which one can edit all attributes of an item (title, price, quantity, unit). Clicking on "Speichern" (save) will save these changes.
There also is a button "Alternativen" (alternatives) located just under the field showing the price. This button, once clicked opens a modal showing alternatives to the current item. This is in case the automatic selection was a bit off.
Deleting items can be done by checking the checkbox next to the title and clicking the button "Artikel löschen" (delete item). It is possible to delete one or many items simultaneously.
Right below the list there is also the sum of the prices of all items on the list.
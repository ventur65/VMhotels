ProgettoVM
Andrea Venturi Matricola n. 78804
Gianluca Maugeri Matricola n. 79300

ISTRUZIONI PER INSTALLAZIONE:
Il progetto è stato sviluppato usando Django 1.8 e MySQL 5.5.

Librerie Esterne da Installare:
	pip install django-phonenumber-field
	pip install django-registration
	pip install django-command-extensions
	pip install django-extensions
	pip install django-bootstrap3
	pip install django-bootstrap3-datetimepicker

Per creare il database si esegua il seguente comando mysql:
CREATE DATABASE progettoVM;

Nel file settings.py l'utente mysql usato è 'admin' con password 'progettodin'.
Se l'utente admin esiste già nel database o se si intende usare un altro utente,
commentare la prima riga del file useradmin.sql e modificarlo opportunamente.
Modificare inoltre con l'utente giusto il file settings.py ai campi USER e PASSWORD
di DATABASES.
In seguito eseguire il comando:
	mysql -u root -p < useradmin.sql

Le forniamo, inoltre un dump del nostro database di django.
Una volta seguiti i passi precedenti, quindi, si proceda con:
	python manage.py syncdb -- Rispondere no alla domanda se creare un superuser --
	python manage.py loaddata db.json
Caricando i dati il superuser che abbiamo creato per accedere all'interfaccia 
admin http://127.0.0.1:8000/admin/ ha come username 'gianluca' e password 'gianluca'.
Per eseguire i test:
	python manage.py test
	
Per far partire il server:
	python manage.py runserver
	
EMAIL:
Di default le email vengono stampate su stdout. Per inviarle effettivamente
commentare l'opzione EMAIL_BACKEND.
	
UTILIZZO SOFTWARE:
Alla pagina iniziale http://127.0.0.1:8000/ si trova la pagina di ricerca
illustrata nella relazione.

Gli utenti che abbiamo creato sono:
OWNERS:
user:pass
owner1:owner1
owner2:owner2
owner3:owner3

CUSTOMERS:
user:pass
customer1:customer1
customer2:customer2

Gli owner possono creare hotel (http://127.0.0.1:8000/hotels/createhotel/) e 
camere nei propri hotel (da pagina dettaglio hotel con bottone 'Add Room').

I customer possono scrivere recensioni su hotel (da pagina dettaglio hotel con
bottone 'Add Review') e fare Reservation (da pagine dettaglio camera con 'Add Reservation').

Se si logga con customer2, nella pagina personale si dovrebbero trovare 3 reservation
effettuate per la stessa stanza, di cui una sola non in coda 
(non ha la scritta --in queue--).
Cliccando sul link nella reservation attiva, si accede alla pagina di dettaglio.
Se si prova ad eliminare tale prenotazione, si potrà notare che le 2 prenotazioni 
rimaste non sono più in coda e, sul terminale, si noteranno le 2 email che sarebbero
state spedite.
Per la spiegazione si veda la sezione sulle Prenotazioni nella Relazione.

Per visualizzare review andare alla pagina http://127.0.0.1:8000/review/19/

Per qualsiasi chiarimento o dubbio non esiti a contattarci all'indirizzo email
con cui il progetto le è stato consegnato.

Cordiali Saluti,
Andrea Venturi
Gianluca Maugeri




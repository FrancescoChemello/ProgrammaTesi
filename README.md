# ProgrammaTesi
Programma di estrazione dati linguistici contenuti nella pagina:

https://www.um.es/lexico-comercio-medieval/index.php

E' presente un file pdf contenente tutta la documentazione.

# Contenuto release:
  - WebScraping.py: il programma che effettua l'estrapolazione dei dati e li salva in un file 'data.xlsx' contenuto nella cartella 'result'.
  - CheckResults.py: un programma extra che controlla che tutti i dati siano stati salvati correttamente _(controlla che tutti i link riportati nel file 'links.txt' siano stati salvati nel file 'data.xlsx' e viceversa)_.
  
  _gli altri file servono per il corretto funzionamento del programma_
  
# Installazione delle librerie:
Per installare le librerie necessarie per l'utilizzo di questo programma si cosiglia di:
  1. Aprire il terminale in modalità amministratore.
  2. Eseguire il comando _pip install beautifulsoup4_ e premere invio.
  3. Eseguire il comando _pip install requests_ e premere invio.
  4. Eseguire il comando _pip install openpyxl_ e premere invio.
  5. Chiudere il terminale e se necessario riavviare il sistema.

# Eseguire il programma:
_(dalla versione 3.2.38 in poi)_

Per eseguire il programma scaricare il file .zip . Estrarre i dati dalla cartella ed avviare il file 'WebScraping.py'. Se si vuole vedere un esempio del funzionamento del programma è consigliato avviarlo in modalità di test. Per farlo digitare 'y' alla prima istruzione. Il tempo di una run in modalità test è di circa 10 minuti.


# Risultati:
I dati linguistici vengono salvati all'interno della cartella 'result' in un file chiamato 'data.xlsx' . I dati che vengono estratti sono:
  - Vocabolo.
  - Definizione: la definizione che spiega il vocabolo.
  - Tipo. 
  - Archivio documenti referenziati: quali documenti sono stati referenziati dal vocabolo e da chi.
  - Numero di documenti referenziati dal vocabolo.
  - URL della pagina.
  - Data di salvataggio del record.

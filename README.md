# ProgrammaTesi
Programma di estrazione dati linguistici contenuti nella pagina https://www.um.es/lexico-comercio-medieval/index.php

E' presente un file pdf contenente tutta la documentazione.

___________________________________________________________

# Contenuto release:
  - WebScraping.py: il programma che effettua l'estrapolazione dei dati e li salva in un file 'data.xlsx' contenuto nella cartella 'result'.
  - CheckResults.py: un programma extra che controlla che tutti i dati salvati estrapolati siano stati salvati correttamente.
  
  _gli altri file servono per il corretto funzionamento del programma_
  
___________________________________________________________

# Eseguire il programma:
_(per versione 3.2.38)_
Per eseguire il programma scaricare il file .zip . Estrarre i dati dalla cartella ed avviare il file 'WebScraping.py'. Se si vuole vedere un esempio del funzionamento del programma è consigliato avviarlo in modalità di test. Per farlo digitare 'y' alla prima istruzione. Il tempo di una run in modalità test è di circa 10 minuti.

___________________________________________________________

# Risultati:
I dati linguistici vengono salvati all'interno della cartella 'result' in un file chiamato 'data.xlsx' . I dati che vengono estratti sono:
  - Vocabolo.
  - Definizione: la definizione che spiega il vocabolo.
  - Tipo. 
  - Documenti referenziati e archivio documenti referenziati: quali documenti sono stati referenziati dal vocabolo e da chi. 
  - URL della pagina.
  - Data di salvataggio del record.

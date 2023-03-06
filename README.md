# ProgrammaTesi
#Librerie
	Nel programma vengono usate le seguenti librerie:
		1. [[BeautifulSoup]] o bs4.
		2. [[Requests]].
		3. [[Openpyxl]].
		4. Datetime.
		5. Os.
		6. System.
		7. Msvcrt.
		8. Random (solo per il test).

#Funzioni
	Nel programma sono presenti le seguenti funzioni:
		1. [[Funzione test]].
		2. [[Funzione initialize]].
		3. [[Funzione searching]].
		4. [[Funzione scraping]].
		5. [[Funzione update]].
		6. [[Funzione save]].
		7. [[Funzione swap]].
		8. [[Funzione logerror]].
		9. [[Funzione table_write]].
		10. [[Funzione remove_link]].

#Struttura
	La struttura del programma può esser riassunta in:
		1. [[Controllo sessioni precedenti]].
		2. [[Ricerca]].
		3. [[Estrapolazione dati]].
		4. [[Apertura link con errore]].
		5. [[Aggiornamento Database]].
    
_______________________________________________________________________________________________________
#Controllo sessioni precedenti

*(costituisce la prima fase del [[Programma Tesi]])*. 

#Definizione 
	In questa fase il programma verifica il contenuto dei file 'lastlink.txt' e 'lastrecord.txt' per poter ripristinare la sessione precedente -> vedi [[Salvataggio sessione]].
	1. Inizialmente il programma controlla il contenuto di 'lastrecord.txt'. Se il file contiene un link e l'utente desiderasse continuare con la sessione precedente, il programma procederà alla fase di [[Estrapolazione dati]] e continuerà con il salvataggio dei record a partire da quello indicato dal file.
			Il programma apre il file 'links.txt', cerca il link contenuto in 'lastrecord.txt' e lo salva nella variabile lastrecord. Successivamente copierà nella variabile link_risultati i valori di 'links.txt' dal indice di lastrecord fino alla fine.
			*index = old_link.index(lastrecord)
			for i in range(index+1, len(old_link)):
				link_risultati.append(i)*
		In caso contrario eliminerà il contenuto di 'lastrecord.txt' ed eliminerà tutti i link contenuti in 'links.txt' che non sono stati salvati -> **questo per mantenere il database consistente**
	2. Se 'lastrecord.txt' è vuoto allora il programma procederà a controllare il contenuto di 'lastlink.txt'. Se contiene un link e l'utente desiderasse contiuare con la sessione precedente, allora il programma continuerà la fase di [[Ricerca]] a partire da dove era stata interrotta. Verrà quindi ricalcolato il punto di partenza della ricerca.
			Il programma salva in 'lastlink' il contenuto del file 'lastlink.txt' e procede come la modalità classica. Dopo la chiamata della [[Funzione initialize]], il programma rimuoverà le pagine già analizzate (ovverto tutte quelle precedenti a 'lastlink')
	3. Se entrambi dovessero essere vuoti il programma partirà in modalità classica seguendo tutte le fasi descritte nel [[Programma Tesi]].
    

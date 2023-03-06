#Chemello Francesco 1219613
#Web Scraping Python

#per webscraping
import bs4, requests
#per log errori
import datetime as dt
#per la scrittura dei risultati in file Excel
import xlsxwriter
#solo per test
import random

import sys, os


#Eccezione per link non è valido
class BeautifulSoupError(Exception):
    def __init__(self, link, code, message = 'Link non valido') -> None:
        self.link = link
        self.code = code
        self.message = message
        super().__init__(self.message)
        


#Funzione di test del programma con alfabeto pseudo random    
def test(num):
    alphabet = ['','a','á','b','c','ç','d','e','é','f','g','h','i','í','j','k','l','m','n','ñ','o','ó','p','q','r','s','t','u','ú','ü','v','w','x','y','z']
    alph = ['']
    for i in range (0, num-1):
        n = random.randint(1, len(alphabet)-1)
        alph.append(alphabet[n])
    return alph


# Ricerca dei vocaboli presenti in 'https://www.um.es/lexico-comercio-medieval'. Verranno mantenuti solo quelli che
# contengono al proprio interno
# input: 
#   -pref - variabile contenente il prefisso dell'url delle pagine di ricerca
#   -link - contiene l'url della sezione di ricerca del sito senza la query string completa
# output: res - lista contenente tutti i link trovati dal campo di ricerca 
def searching(pref, s_link):
    res = []
    #http request -get http
    response = requests.get(s_link)
    response.raise_for_status()
    #estraggo il testo della risposta in formato html
    # soup = bs4.BeautifulSoup(response.text, 'html.parser')          MODIFICATO
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    #sezione risultati
    risultati = soup.find('article', class_='resultados')
    #trovo tutti gli hyperlink della sezione risultati
    a_risultati = risultati.find_all('a')
    #gestione link ottenuti
    for i in a_risultati:
        vrf = str(i.get('href'))
        if pref in vrf:
            url = vrf
            id_str = str(url[len(pref):len(url)])
            id_len = len(id_str)
            if id_len > 0 and vrf not in res:        #evito di copiare le pagine che sono senza vocaboli
                res.append(vrf)
    return res


# Scraping della pagina web. Vengono estratti:
#   -VOCABOLO: la parola interessata
#   -DEFINIZIONE: la descrizione del termine
#   -TIPO: la tipologia del termine
#   -DOCUMENTI REFERENZIATI: eventuali reference legate alla parola
#   -ARCHIVIO DOCUMENTI REFERENZIATI: contiene tutti i documenti che sono stati referenziati
# input: l - link della pagina da analizzare
# output: None
def scraping(l):
    res = []
    #lettura pagina html
    response = requests.get(l, allow_redirects=False)   #blocco reindirizzamento a siti esterni
    response.raise_for_status()     #per il lancio delle eccezioni HTTP durante la creazione 
    if response.status_code != 200:     #HTTP response 200 OK   
        raise BeautifulSoupError(l, response.status_code) #lancio eccezione
    page = bs4.BeautifulSoup(response.content, 'html.parser')
    soup = page.find('article', class_='resultados')    #lavoro su una porzione della pagina
    #estrapolo il vocabolo
    vocabolo = ''
    v = soup.find('h3', class_='lexema_title')
    if v is not None:
        vocabolo = v.text.strip()
    res.append(vocabolo)
    #estraggo la definizione
    definizione = ''
    df = soup.find('p',  class_='descripcion')
    if df is not None:
        definizione = df.text.strip()
        if str('\n') in definizione:
            definizione.replace('\n', ' ')
    res.append(definizione)
    #estraggo il tipo
    tipo = ''
    t = soup.find('span', class_='tipo')
    if t is not None:
        tipo = t.text.strip()
    res.append(tipo)
    #estraggo reference
    reference = ''
    def_ref = ''
    rf = soup.find('div',  id='detalle_imagenes_lexema')
    if rf is not None:
        h4 = rf.find('h4')
        reference = h4.text.strip()
        #estraggo definizione reference
        d_ref = rf.findAll('p')
        for d in d_ref:
            def_ref += d.text.strip()
        reference += ' : ' + str(def_ref)
    res.append(reference)
    #estraggo archivio documenti referenziati
    arch_def = ''
    arch = soup.find('div', id='imagenes')
    if arch is not None:
        a_risultati = arch.find_all('a', alt=True)
        #gestione alt tags ottenuti
        for i in a_risultati:
            vrf = str(i.get('alt'))
            arch_def +=str(vrf) + '; '
    res.append(arch_def)
    #PROVA RECUPERO DIV SENZA CLASSE --------------------------------!!!
    #estraggo reference
    reference = ''
    def_ref = ''
    rf = soup.find('div', id=None)
    if rf is not None:
        h4 = rf.find('h4')
        if h4 is not None:
            reference = h4.text.strip()
            #estraggo definizione reference
            d_ref = rf.findAll('p')
            for d in d_ref:
                def_ref += d.text.strip()
            reference += ' : ' + str(def_ref)
    res.append(reference)
    #estraggo archivio documenti referenziati
    arch_def = ''
    arch = soup.find('div', id='imagenes_jmarch')
    if arch is not None:
        a_risultati = arch.find_all('a', alt=True)
        #gestione alt tags ottenuti
        for i in a_risultati:
            vrf = str(i.get('alt'))
            arch_def +=str(vrf) + '; '
    res.append(arch_def)
    res.append(l)
    return res


#Per la gestione di eventuali errori nello scraping viene scritto un log degli errori
#input:
#   -l: variabile che contiene il link della pagina interessata da errore
#   -scode: contiene il codice di errore
def logerror(l, exception):
    absolute_path = os.path.dirname(__file__)
    full_path = os.path.join(absolute_path, logerrori_path)
    date = dt.datetime.now()
    now = '[' + str(date.day) + '-' + str(date.month) + '-' + str(date.year)+']\n'
    with open(full_path, 'a', encoding='utf-8') as f1:
        f1.write(now + str(l) + '\nStatus code: '+str(exception))
        f1.write('\n')
    
#Scrittura dei dati estrapolati in un file excel. I file vengono scritti per righe 
#input:
# -res: contiene i dati estratti dalla funzione scraping (id, vocabolo, definizione,
#   tipo, reference, definizione reference ed immagini)
# -worksheet: contiene la pagina di lavoro excel sulla quale verranno scritti i record
# -cont: contatore della riga di scrittura
#output: None
def table_write(res, worksheet, row):
    column = 0
    # iterating through content list
    for item in res:
        # write operation perform
        worksheet.write(row, column, item)
        column += 1
        
        
#Rimuove un link dall'elenco
#input: 
#   -link: contiene il link da rimuovere
#output: None         
def remove_link(link, exception):
    absolute_path = os.path.dirname(__file__)
    full_path = os.path.join(absolute_path, links_path)    
    with open(full_path, 'r', encoding='utf-8') as file:
        filedata = file.read()
    filedata = filedata.replace(str(link), '\r')
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(filedata)
        logerror(link, exception)


#!--    MAIN
link = 'https://www.um.es/lexico-comercio-medieval/index.php/search/?busqueda='
prefisso = 'https://www.um.es/lexico-comercio-medieval/index.php/v/lexico/'
cont_res = 0
#list per la query string
alphabet = ['','a','á','b','c','ç','d','e','é','f','g','h','i','í','j','k','l','m','n','ñ','o','ó','p','q','r','s','t','u','ú','ü','v','w','x','y','z']
#indici per ciclo for ricerca
in_a1 = 1
in_a2 = 0
#path dei file che il programma usa -> sostituiscono var relative_path
absolute_path = os.path.dirname(__file__)
lastlink_path = 'data\lastlink.txt'
lastrecord_path = 'data\lastrecord.txt'
links_path = 'data\links.txt'
logerrori_path = 'data\logerrori.txt'
data_path = 'result\data.xlsx'

#!--    OLD START
# link_risultati = test(5, prefisso, link)            #TEST

x = input('Avviare il programma in modalità di test? (y/n)\nQuesto cancellerà i salvataggi precedenti!\n\n-> ') 
#modalità di test
if x.casefold() == 'y':
    print('Programma in modalità test')
    alphabet = test(5)
    #calcello il file 'links.txt' perché non serve per la modalità test
    full_path = os.path.join(absolute_path, links_path)
    with open(full_path, 'r+', encoding='utf-8') as file:
        file.seek(0)
        file.truncate(0)
    #cancello file 'data.xlsx' in quanto non serve il precedente per la modalità test
    full_path = os.path.join(absolute_path, data_path)
    if os.path.exists(full_path):
        os.remove(full_path)
else:
    print('Programma in modalità classica')
#raccolta dati
#anche se non da risultati comunque la pagina html contiene il campo <article class='resultados'>...</article>
#pre ciclo di ricerca:
#   2- if -> il file non è vuoto allora:
#       true -> chiedo utente se vuole continuare la ricerca che era stata precedentemente interrotta
#           if -> decide di continuare:
#               true -> recupero link dal file, ricalcolo indici array ricerca e svuoto file
#               false -> svuoto file
#       false -> skip al punto successivo 'ciclo di ricerca' e svuoto file
#   1- open file 'lastlink.txt' dove è stato salvato l'ultimo link che è stato analizzato
    full_path = os.path.join(absolute_path, lastlink_path)
    with open(full_path, 'r+', encoding='utf-8') as file:
        if file.read() == '':
            #non devo modificare il valore degli indici, il file è vuoto 
            pass
        else:
            #file non vuoto
            x = input('Vuoi continuare la ricerca che era stata interrotta l ultima volta? (y/n)\n\n-> ')
            if x.casefold() == 'y':
                #continuo la precedente 
                filedata = file.read()  #è una stringa?
                filedata = filedata.replace(prefisso, '')   #rimuovo il prefisso
                if len(filedata) < 2:
                    #ho una sola lettera
                    in_a1 = alphabet.index(filedata)
                else:
                    #ho due lettere
                    in_a1 = alphabet.index(filedata[0:1])
                    in_a2 = alphabet.index(filedata[1:len(filedata)])
                    #cancello contenuto del file
                    with open(full_path, 'r+', encoding='utf-8') as file:
                        file.seek(0)
                        file.truncate(0)       
            else:
                pass
#salvataggio risultati in file di testo
full_path = os.path.join(absolute_path, links_path)
#estrazione elementi da testo salvati in lista python con rimozione carattere a capo
old_link = [r.rstrip('\n') for r in open(full_path, encoding='utf-8')]
link_risultati = []
try:
    #nuovo ciclo di ricerca:    
    #   1- invoco la funzione di ricerca 'searching' per la ricerca di link
    #   2- salvo nel file di testo 'links.txt' i valori restituiti dalla funzione 'searching'
    #   3- ripeto
    tot = (len(alphabet)-1)*len(alphabet)  #nummero possibili combinazioni
    cont = 1
    r_link = ''
    for a1 in range(in_a1, len(alphabet)):
        for a2 in range(in_a2, len(alphabet)):
            #genero nuovo link di ricerca
            r_link = str(link+alphabet[a2]+alphabet[a1])
            sys.stdout.write('\r')
            percentage = (cont / tot)*100
            sys.stdout.write('Sto eseguendo la ricerca: '+str(float(f'{percentage:.2f}'))+'%')
            sys.stdout.flush()
            res = searching(prefisso, r_link)
            for l in res:
                if l not in old_link and l not in link_risultati:
                    #apertura file in modalità append per scrittura con raw string come percorso
                    with open(full_path, 'a', encoding='utf-8') as f1:
                        #nuovo elemento da aggiungere al file di testo
                        f1.write(l)
                        f1.write('\n')
                    cont_res += 1
                    link_risultati.append(l)      #aggiorno old_link per tenerlo aggiornato
            cont += 1
    del cont, tot, r_link
    #gestione degli errori:
    #   se il programma si pianta (causa connection fail) il programma deve salvare l'ultimo link cercato 
    #   (quello che è fallito) in 'lastlink.txt' -> salvato in una variabile!
#se avviene un errore in connessione non è possibile continuare l'attività    
except requests.exceptions.RequestException as e:
    full_path = os.path.join(absolute_path, lastlink_path)
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(r_link)  #l'ultimo link analizzato
    print('\n'+str(e)+'\nPer favore riprovare')
    sys.exit(1)     #uscita dal programmaa
 
print('\nRicerca completata')
print('Sono stati trovati '+str(cont_res)+' risultati nuovi')
#estrapolazione dei dati dalle pagine html salvate in links.txt
record = ''
cont = 0        #la scrittura in 'A1' è cella [0,0]
link_error = []
#apertura del file excel
full_path = os.path.join(absolute_path, data_path)
excel_file = xlsxwriter.Workbook(full_path)
worksheet = excel_file.add_worksheet()
worksheet.write('A1', 'VOCABOLO')
worksheet.write('B1', 'DEFINIZIONE')
worksheet.write('C1', 'TIPO')
worksheet.write('D1', 'DOCUMENTI REFERENZIATI -1')
worksheet.write('E1', 'ARCHIVIO DOCUMENTI REFERENZIATI -1')
worksheet.write('F1', 'DOCUMENTI REFERENZIATI -2')
worksheet.write('G1', 'ARCHIVIO DOCUMENTI REFERENZIATI -2')
worksheet.write('H1', 'URL PAGINA')
for l in link_risultati:
     if l not in old_link:
        try:
            sys.stdout.write('\r')
            sys.stdout.write('Estrapolazione dati: '+'['+str(cont+1)+'/'+str(cont_res)+']')
            sys.stdout.flush()
            res = scraping(l)
            cont += 1
            table_write(res, worksheet, cont)
        except requests.exceptions.ConnectTimeout:
            link_error.append(l)
            cont_res -= 1
            continue
        except BeautifulSoupError as e:
            logerror(l, e)
            cont_res -= 1
            #rimuovo il link non valido
            remove_link(l, e)
            continue
        except requests.exceptions.RequestException as e:
            logerror(l, str(e))     #report in logerror
            cont_res -= 1
            remove_link(l, e)
            continue         
#gestione pagine non caricate
cont_res = len(link_error)
c = 1
if len(link_error) > 0:
    fail = 0
    maxfail = len(link_error) + (len(link_error) // 2)
    while fail < maxfail and len(link_error) > 0:
        #ripeto il codice
        l = link_error[0]
        try:
            #rifaccio l'analisi
            sys.stdout.write('\r')
            sys.stdout.write('Riapertura link con errore connessione'+'['+str(c)+'/'+str(cont_res)+']')
            sys.stdout.flush()
            res = scraping(l)
            cont += 1
            table_write(res, worksheet, cont)
            link_error.remove(l)
        except requests.exceptions.ConnectTimeout:
            logerror(l, 'requests.exceptions.ConnectTimeout')
            #riprovo successivamente a ricollegarmi alla pagina
            link_error.remove(l)
            link_error.append(l)
            continue
        except BeautifulSoupError as e:
            logerror(l, e)
            link_error.remove(l)
            continue
        except requests.exceptions.RequestException as e:
            logerror(l, str(e))     #report in logerror
            cont_res -= 1
            link_error.remove(l)
            continue
    #rimozione record che non è stato possibile gestire per errore connessione
if len(link_error) > 0:
    for l in link_error:
        remove_link(l)
#chiusura file di testo
excel_file.close()
print('\nEstrapolazione dati completata')
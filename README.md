# Dots and Boxes: Un avversario ”intelligente”

## Roberto Falcone

## r.falcone13@studenti.unisa.it

## 1 Introduzione

## 1.1 Contesto e Scopo del Progetto

Il presente report descrive il progetto finalizzato alla realizzazione di un al-
goritmo in grado di giocare in modo efficiente ad un gioco, con l’obiettivo di
ottenere buone prestazioni contro un avversario umano. Il cuore dell’algoritmo é
basato sulla tecnica di ricerca di alberi decisionali minmax e alpha-beta pruning.
Questo approccio di intelligenza artificiale oggigiorno é ampiamente utilizzato
per affrontare sfide riguardanti giochi e altre applicazioni che richiedono un
ragionamento strategico ottimale.

## 1.2 La Rilevanza della Teoria dei Giochi

La teoria dei giochi é un campo fondamentale nell’intelligenza artificiale, in cui
si studiano le strategie e i comportamenti di agenti razionali in situazioni com-
petitive o cooperative. La teoria dei giochi offre un approccio matematico e
formale per analizzare situazioni decisionali, identificare le migliori strategie e
comprendere i risultati che emergono da interazioni complesse tra i giocatori.
Questa teoria é di fondamentale importanza nello sviluppo di algoritmi intelli-
genti in quanto consente di modellare il comportamento razionale degli agenti e
trovare le migliori azioni da intraprendere.

## 1.3 Applicazioni dei Giochi nei Problemi Complessi

I giochi non sono solo fonte di divertimento, ma costituiscono anche una preziosa
piattaforma di studio per sviluppare e valutare algoritmi di intelligenza artifi-
ciale. La vasta gamma di giochi, dai deterministici a quelli non deterministici,
da quelli perfettamente informati a quelli parzialmente informati, permette di
affrontare una molteplicit`a di scenari che riflettono le sfide presenti in numerosi
problemi reali.


### 1.4 La Scelta del Gioco

Come caso di studio per questo progetto é stato selezionato il gioco ”Dots
and Boxes”, che offre una piattaforma semplice e allo stesso tempo ricca di
complessit`a per testare l’efficacia dell’algoritmo di alpha-beta pruning.

## 2 Background

### 2.1 Dots and Boxes

```
Figure 1: Tabellone di Dots and Boxes vuoto
```
”Dots and Boxes” é un gioco di carta e matita per due o più giocatori. Partendo
da una griglia vuota, formata solo da punti, i giocatori possono, a turno, inserire
una linea orizzontale o verticale tra due punti non ancora collegati. Quando uno
dei due giocatori traccia il quarto lato di un quadrato ottiene un punto e marca
il quadrato come conquistato. La partita termina quando non é più possibile
disegnare linee all’interno della griglia e vince il giocatore che ha ottenuto più
punti, ossia quello che ha conquistato più quadrati.
Non ci sono personaggi o oggetti in gioco, il che rende il giocoastratto.
Poich ́e non ci sono elementi casuali o aleatori nel gioco, il risultato di ogni
mossa é interamente prevedibile in base alla situazione attuale sulla griglia e
alle azioni dei giocatori, perciò édeterministico. Ogni giocatore può vedere la
griglia completa e le linee gi`a disegnate. Ciò significa che entrambi i giocatori
hanno una visione chiara e completa della situazione di gioco, il che influisce
sulle loro decisioni tattiche e strategiche, da questo si evince che il gioco siaad
informazione completa.
Esistono due varianti di gioco: una prevede che, una volta completato un
quadrato, il turno rimanga al giocatore che ha guadagnato il punto, che può
quindi completare altri quadrati finch ́e gli é possibile. L’altra invece, mantiene
l’alternanza dei turni tra i giocatori, indipendentemente da chi conquista un
punto durante la partita.


Si é scelto di prendere in analisi la prima variante perch ́e ritenuta sicuramente
più sfidante.

2.1.1 Il gioco nel dettaglio

La maggior parte delle argomentazioni di questa sezione deriva dagli studi del
professore di matematica e computer science dell’Universit`a della California,
Elwyn Berlekamp, che ha dedicato la propria carriera allo studio di giochi
come ”Fox and Geese”, ”Go” e, per l’appunto, ”Dots and Boxes”.

```
Figure 2: Elwyn Berlekamp
```
Il gioco, secondo il professore Berlekamp, ha un paio di meccaniche che lo
rendono abbastanza unico e complesso da analizzare: la prima, la possibilità
continuare a muovere una volta conquistato un quadrato: la seconda, i due
giocatori hanno come obiettivo quello di fare più punti possibili e non di effettu-
are l’ultima mossa, tuttavia, come vedremo più avanti nel report, questi due
obiettivi sono implicitamente collegati.
Prima di tutto c’é bisogno di dare la definizione dicatena. Quando un gioc-
atore completa un quadrato appartenente ad una catena, cattura quel quadrato
e può continuare a catturare quadrati per tutta la lunghezza della catena. Le
catene possono essere di lunghezza variabile, da una singola cella a una sequenza
più lunga di quadrati adiacenti, e possono cambiare direzione o addirittura in-
tersecarsi. L’obiettivo ”nascosto” del gioco, come vedremo, é creare catene
lunghe e complesse per catturare il massimo numero di caselle e segnare più
punti rispetto all’avversario.

2.1.2 Le due fasi di gioco

La partita si divide in 2 fasi:

- La prima fase é la fase nella quale i giocatori cercano di creare catene ed
    evitare di regalare punti all’avversario (quindi marcando il terzo lato di un
    quadrato, mossa che porterà l’avversario a completare il quadrato stesso
    oltre che continuare con la consueta mossa).


- Durante la seconda fase invece i giocatori si occupano soltanto di com-
    pletare le catene formate, cercando di aggiudicarsi quelle più lunghe.

```
(a) (b)
```
Figure 3: Figura (a) mostra la fine della prima fase; Figura (b) mostra la fine
della seconda fase

Questa divisione in due fasi distinte non é facilmente riconoscibile da un
giocatore alle prime armi.
La fase più ”intuitiva” delle due risulta essere la prima. In questa fase
l’obiettivo, agli occhi di un giocatore principiante, é cercare di non regalare
punti all’avversario, segnando il terzo lato di un quadrato.
Le ”buone maniere” in questa fase, sono quindi:

- Se possibile, segnare il quarto lato di un quadrato
- Evitare di segnare il terzo lato di un quadrato
Per un giocatore esperto invece, la fase più interessante é proprio la seconda,
perch ́e é proprio in vista di questa fase che quest’ultimo cerca di costruire più
o meno catene lunghe.

2.1.3 Regola della catena lunga

Esiste una regola che, se sfruttata a dovere, può avvicinare alla vittoria il gioc-
atore che la applica, ossiala regola della catena lunga: supponiamo che il
campo di gioco sia un rettangolo dimrighe encolonne e quindi sia composto
dam·nquadrati. Se siamchensono pari, allora il primo giocatore dovrebbe
cercare di rendere dispari il numero di catene lunghe. Se anche solo uno tramo
né dispari, allora il primo giocatore dovrebbe cercare di rendere pari il numero
di catene lunghe. Per catene lunghe si intende qualsiasi catena che superi la
lunghezza di 3 quadrati.


Inoltre, in caso di una griglia conm=n, le due dimensioni dipendono
strettamente dal numero di punti con i quali la si é costruita:

```
m=n= #dots− 1
```
Quindi se il numero di punti é dispari alloramednsaranno pari, cos`ı come se
il numero di punti é pari alloramednsaranno dispari.
Riassumendo formalmente il numero di catene lunghe desiderate é:

- PARI: per il primo giocatore se il numero di punti é pari, per il secondo
    giocatore se il numero di punti é dispari
- DISPARI: per il primo giocatore se il numero di punti é dispari, per il
    secondo giocatore se il numero di punti é pari


## 3 Implementazione

Il fine del presente progetto é stato l’ideazione e l’implementazione di un algor-
itmo che dimostri un’efficace abilità di gioco nel contesto specifico. L’algoritmo
deve dimostrare la capacità di eseguire il gioco con precisione e competenza,
evitando di cedere all’avversario vantaggi nel corso della fase di costruzione
delle catene. Si richiede che l’algoritmo rispetti le convenzioni di gioco preced-
entemente delineate e che, al contempo, punti all’obiettivo di creare un numero
ottimale di catene lunghe, avvicinandosi cos`ı alla vittoria della partita. Questi
criteri sono dettagliatamente esposti nella sezione2.1.2e2.1.3del documento.
Ovviamente, l’algoritmo deve infine dimostrare l’abilità di accumulare un quant-
itativo massimo di punti possibile.

### 3.1 GUI

Per la realizzazione dell’interfaccia grafica utente (GUI) nel contesto di questo
progetto, é stata adottata la soluzione proposta da Aqueel Anwar, la quale é
disponibile nella repository GitHub Dots-and-Boxes by aqueelanwar.

```
(a) (b)
```
Figure 4: Figura (a) mostra la GUI durante la fase di gioco; Figura (b) mostra
come la GUI visualizza il vincitore della partita

L’interfaccia é molto semplice, permette al giocatore di cliccare sulla linea che
vuole marcare e colora eventuali celle completate con il colore del giocatore che
ha segnato il punto, blu per il primo giocatore, rosso per il secondo giocatore.
Nel momento in cui tutte le celle sono state conquistate la GUI passa alla
visualizzazione del risultato della partita, annunciando il vincitore e mostrando
i punteggi di entrambi i giocatori. Per effettuare un’altra partita basterà cliccare
ovunque sulla dashboard.


### 3.2 CPU solo alpha-beta

Il primo bot realizzato fa utilizzo soltanto dell’algoritmo di alpha-beta pruning.
E implementato dalla classe E1` CPU() e per la valutazione di ogni mossa si
limita a calcolare la differenza di punteggio tra il giocatore che sta giocando e
l’avversario.

```
Figure 5: Funzione per la valutazione di una mossa del primo bot
```
### 3.3 CPU alpha-beta e regola della catena lunga

Il secondo bot aggiunge all’algoritmo di alpha-beta pruning l’euristica della
catena lunga, presentata nella sezione2.1.3. L’euristica é stata implementata
pesando maggiormente le mosse che avrebbero avvicinato il giocatore ad un
numero corretto di catene lunghe. Inoltre, é stato aggiunto un parametro
CHAINPOINTS per pesare correttamente l’influenza dell’euristica rispetto al
comportamento iniziale del bot.

```
Figure 6: Funzione per la valutazione di una mossa del secondo bot
```

### 3.4 CPU con predizione di conquista delle catene

Il terzo bot invece cerca di predire quali catene verranno conquistate dai due
giocatori. In questo caso alla differenza tra i punteggi dei giocatori vengono
aggiunti i punteggi relativi al completamento di tutte le catene dispari o pari,
in dipendenza da se il giocatore sarà il primo a iniziare il completamento delle
catene o meno. Questo ragionamento si basa sul fatto che, una volta completata
una catena, sia necessario cederne un’altra all’avversario (ovviamente lasciando
a quest’ultimo le più piccole sulla griglia). Per l’implementazione infatti, é
bastato ordinare le catene all’interno di una lista per poi attribuire il punteggio
di quelle in posizioni dispari al primo giocatore che effettuasse la mossa e, di
conseguenza, il punteggio di quelle pari al giocatore avversario.

```
Figure 7: Funzione per la valutazione di una mossa del terzo bot
```

### 3.5 Selezione dei giocatori

All’interno della classe main é possibile selezionare la tipologia dei due giocatori:
PvP mode (giocatore contro giocatore); PvB mode (giocatore contro bot); BvB
mode (bot contro bot)

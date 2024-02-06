# TomatoAI

TomatoAI è un progetto Django che può essere eseguito sia in un ambiente Dockerizzato sia in modo locale senza Docker. Utilizza Django per il backend, Postgres come database quando operato in modalità non di sviluppo con Docker, e SQLite per la modalità di sviluppo locale. Nginx viene utilizzato per servire file statici e come reverse proxy quando si opera con Docker.

## Prerequisiti

- Docker e Docker Compose installati (per l'esecuzione con Docker).
- Python 3.10 installato (per l'esecuzione locale senza Docker).

---

## Configurazione del File `.env`

Prima di avviare il tuo progetto, sia in locale che con Docker, devi configurare le variabili d'ambiente creando un file `.env` nella directory principale del progetto. Di seguito sono forniti due esempi di configurazione: uno per lo sviluppo locale e uno per l'uso con Docker.

### Configurazione per Sviluppo Locale

Se stai lavorando in modalità di sviluppo locale e desideri utilizzare SQLite come database, puoi configurare il tuo file `.env` come segue:

```
DJANGO_SECRET_KEY=<inserisci_valore>
DEBUG=True|False
DEVELOPMENT_MODE=True
ALLOWED_HOSTS=<inserisci_valore> # Come stringa separata da virgole, es. "localhost,127.0.0.1"
```

Nota: In `DEVELOPMENT_MODE=True`, il progetto utilizzerà SQLite come database, che non richiede i campi `DB_*`.

### Configurazione Raccomandata per Docker

Quando si opera con Docker, è consigliato utilizzare Postgres come sistema di gestione del database per garantire la persistenza dei dati tra i riavvii del container. Configura il tuo file `.env` con i seguenti valori per un ambiente Dockerizzato:

```
DJANGO_SECRET_KEY=<stringa-di-32-caratteri>
DEBUG=False # Mettere a True solo se necessario per il debug
DEVELOPMENT_MODE=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_PASSWORD=password
DB_DATABASE=tomatoai
DB_USER=tomatoai
```

Utilizzando questa configurazione, ti assicuri che l'applicazione sia pronta per la produzione con Docker, con impostazioni ottimali per sicurezza, performance e compatibilità.

---

Assicurati di sostituire `<inserisci_valore>` e `<stringa-di-32-caratteri>` con i valori effettivi che intendi utilizzare. Questa distinzione tra le configurazioni assicura che il tuo ambiente sia configurato correttamente in base al contesto di sviluppo o produzione in cui stai lavorando.

---


## Lanciare il Progetto con Docker

### Passo 1: Costruire i container

Per costruire le immagini Docker necessarie per il tuo progetto, esegui il comando:

```bash
docker-compose build
```

Questo comando legge il file `docker-compose.yml`, costruisce le immagini per i servizi definiti che non sono ancora stati costruiti o che hanno subito modifiche.

### Passo 2: Avviare i servizi

Per avviare i servizi definiti nel tuo `docker-compose.yml`, esegui:

```bash
docker-compose up -d
```

L'opzione `-d` avvia i container in background, permettendoti di continuare a utilizzare il terminale. Se preferisci visualizzare i log dei container in tempo reale nel terminale e non avviarli in background, puoi omettere l'opzione `-d`:

```bash
docker-compose up
```

Utilizzando il comando senza `-d`, i log di tutti i servizi avviati con `docker-compose` verranno stampati nel terminale. Per interrompere l'esecuzione, puoi semplicemente premere `CTRL+C`.

Il servizio Nginx, configurato nel tuo docker-compose.yml, sarà accessibile sulla porta 8001 del tuo host. Ciò significa che puoi accedere all'applicazione Django tramite il tuo browser all'indirizzo http://localhost:8001.

### Fermare i servizi

Per fermare i container e rimuovere i container, le reti create da `docker-compose up`, esegui:

```bash
docker-compose down
```

Se desideri rimuovere anche i volumi creati (per esempio, per cancellare i dati persistenti del database o i file statici), puoi aggiungere l'opzione `--volumes` (o `-v` abbreviato):

```bash
docker-compose down --volumes
```

Questo comando elimina tutti i container, le reti e i volumi definiti nel `docker-compose.yml` per il tuo progetto, assicurando che nessun dato persistente rimanga sul tuo sistema se desideri una pulizia completa.

---

## Lanciare il Progetto Localmente (Senza Docker)

### Passo 1: Creazione del Virtual Environment

```bash
python3.10 -m venv env
source env/bin/activate
```

### Passo 2: Installazione delle Dipendenze

```bash
pip install -r requirements.txt
```

### Passo 3: Avviare il Progetto Django

Configura il file `.env` come descritto sopra. Se `DEVELOPMENT_MODE=True`, il progetto utilizzerà SQLite. Esegui i seguenti comandi per avviare il progetto:

```bash
python manage.py migrate
python manage.py collectstatic --no-input  # Questo passaggio è opzionale se DEBUG=True
python manage.py runserver
```

Questo avvierà il server di sviluppo Django sulla porta 8000, rendendo l'applicazione accessibile all'indirizzo [http://localhost:8000](http://localhost:8000).

---

## Visualizzazione della Documentazione API con Swagger

TomatoAI utilizza Swagger UI per offrire una documentazione interattiva e testabile delle API. Una volta avviato il progetto, sia in un ambiente Dockerizzato sia in un ambiente di sviluppo locale, puoi accedere alla documentazione API Swagger all'URL `/swagger` del tuo host.

### Come Accedere a Swagger UI

- **Con Docker**: Assicurati che il progetto sia avviato con Docker e che Nginx sia configurato per servire l'applicazione sulla porta 8001. Puoi visualizzare Swagger UI navigando a [http://localhost:8001/swagger](http://localhost:8001/swagger).

- **Senza Docker**: Se stai eseguendo il progetto localmente senza Docker, assicurati che il server di sviluppo Django sia in esecuzione. Puoi accedere a Swagger UI all'indirizzo [http://localhost:8000/swagger](http://localhost:8000/swagger), assumendo che il server di sviluppo sia configurato per utilizzare la porta predefinita 8000.

Swagger UI fornisce una panoramica completa delle API disponibili, consentendo di esplorare i vari endpoint, i loro parametri, le risposte attese e di effettuare richieste di prova direttamente dall'interfaccia utente.

---

## Integrazione con GitHub Actions

Per migliorare la qualità del codice e garantire che le modifiche non introducano regressioni, TomatoAI utilizza GitHub Actions per automatizzare l'esecuzione dei test. La pipeline è configurata per scattare automaticamente al push di nuovi commit sulla repository e alla creazione di pull request.

### Dettagli della Pipeline

La pipeline GitHub Actions esegue i seguenti passaggi:

- Installazione delle dipendenze necessarie per il progetto.
- Avvio dei servizi necessari, come il database.
- Esecuzione dei test del progetto Django tramite il comando `pytest`.

Questa automazione aiuta a rilevare precocemente problemi e errori, facilitando lo sviluppo di un codice più robusto e affidabile.

### Come Funziona

- **Al Push**: Ogni volta che un nuovo commit viene pushato sul branch main della repository, la pipeline GitHub Actions viene attivata per eseguire i test.
- **Alla Creazione di Pull Request**: Quando viene creata una pull request, la pipeline verifica automaticamente i cambiamenti proposti eseguendo i test. Questo assicura che le modifiche non rompano la funzionalità esistente prima che la pull request venga accettata e mergiata.

### Risultati

I risultati dell'esecuzione della pipeline sono visibili direttamente su GitHub, nella sezione Actions della tua repository. Qui puoi vedere se i test sono stati superati con successo o se sono emersi errori che richiedono attenzione.

---

Con l'integrazione di GitHub Actions, TomatoAI si avvale di un processo di integrazione continua (CI) per mantenere elevati standard di qualità del codice e facilitare il processo di revisione delle pull request.
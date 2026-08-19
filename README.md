# Σύστημα Ανακλήσεως

Μια εφαρμογή σχεδιασμένη για τις ανάγκες Πολεμικών Πλοίων/ Ναυτικών Υπηρεσιών με την οποία οι αντίστοιχοι προϊστάμενοι θα μπορούν να έχουν πρόσβαση στα στοιχεία επικοινωνίας των υφισταμένων τους, ώστε να είναι ευκολότερη η ενημέρωση τους για καταστάσεις ανάκλησης/ ανάγκης/ ενημέρωσης.

Σημείωση: για το σχεδιασσμό της εφαρμογής χρησιοποιήθηκαν εικονικά στοιχεία χρηστών και πλοίο το οποίo δεν είναι πλεόν σε υπηρεσία.

# Personel Recall App

An application designed for the needs of warships/naval services, enabling senior officers to access their subordinates’ contact details so that communication regarding recalls, emergencies or updates can be carried out more easily.

Note: For the design of the app, virtual user data and decommission ship were used.


# Ασφάλεια

- Authentication με Login.
- Authorization βάσει ρόλου: `admin` και `viewer`.
- Αρχικός λογαρισμός (admin): `Ύπαρχος` / `Admin123!` — σε εφαρμοφή από πραγματική υπηρεσία το username και το password θα αλλάξουν από τον αντίστοιχο χρήστη.

# Security

- Authentiication via LOGIN.
- AUthorization based on role: `admin` και `viewer`.
- Initial Account (admin) : `Ύπαρχος` (Executive Officer) / `Admin123!` - in case of real usage username and password shall be changed by the user.


# Εκκίνηση με Docker (προτεινόμενη)

Προϋπόθεση: εγκατεστημένο και ενεργό το Docker Desktop.

```powershell
docker compose up --build
```

Ανοίξτε το `http://localhost:5000`. Η βάση δεδομένων αποθηκεύεται σε Docker volume (`organization_data`) και δεν χάνεται όταν το container σταματήσει. Για τερματισμό πατήστε `Ctrl+C` και, αν χρειαστεί, εκτελέστε `docker compose down`.

Για παραγωγική χρήση ορίστε ένα ισχυρό `SECRET_KEY` πριν την εκκίνηση:

```powershell
$env:SECRET_KEY = "ένα-ισχυρό-τυχαίο-μυστικό"
docker compose up --build -d
```

# Docker Quickstart

Prerequisit: Docker Desktop App installed and running

```powershell
docker compose up --build
```
Open `http://localhost:5000`. The Data Base is saved on a Docker Volume (`organization_data`) and is not lost if the container is terminated. TO terminate press `Ctrl+C`, and if needed execute `docker compose down`.

in case of real usage, set a strong `SECRET_KEY` before starting :


```powershell
$env:SECRET_KEY = "ένα-ισχυρό-τυχαίο-μυστικό"
docker compose up --build -d
```


# Εκκίνηση χωρίς Docker

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Ανοίξτε το `http://127.0.0.1:5000`.


# Native Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.



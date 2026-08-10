# Σύστημα Ανακλήσεως

Μια εφαρμογή σχεδιασμένη για τις ανάγκες Πολεμικών Πλοίων/ Ναυτικών Υπηρεσιών με την οποία οι αντίστοιχοι προϊστάμενοι θα μπορούν να έχουν πρόσβαση στα στοιχεία επικοινωνίας των υφισταμένων τους, ώστε να είναι ευκολότερη η ενημέρωση τους για καταστάσεις ανάκλησης/ ανάγκης/ ενημέρωσης.

## Ασφάλεια

- Authentication με Login.
- Authorization βάσει ρόλου: `admin` και `viewer`.
- Αρχικός λογαριασμός/ admin: `Ύπαρχος` / `Admin123!` — σε εφαρμοφή από πραγματική υπηρεσία το username και το password θα αλλάξουν.

## Εκκίνηση με Docker (προτεινόμενη)

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

## Εκκίνηση χωρίς Docker

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Ανοίξτε το `http://127.0.0.1:5000`.

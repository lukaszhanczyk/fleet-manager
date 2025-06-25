# Fleet Manager IoT - Projekt

## Opis biznesowy

Fleet Manager to innowacyjny system IoT dla firm zarządzających flotą pojazdów.  
Pozwala w czasie rzeczywistym monitorować lokalizację, prędkość oraz stan paliwa każdego pojazdu.  
Dane są przesyłane przez urządzenia IoT (lub symulator) do chmury Google Cloud, gdzie są przechowywane i analizowane.  
System umożliwia szybką reakcję na zdarzenia oraz optymalizację kosztów operacyjnych i tras przejazdu.  

---

## User Stories

- **Jako menadżer floty**, chcę otrzymywać aktualne dane lokalizacyjne pojazdów, aby efektywnie zarządzać logistyką.  
- **Jako kierowca**, chcę, aby moje urządzenie IoT automatycznie raportowało moją pozycję i stan pojazdu bez konieczności ręcznego wpisywania danych.  
- **Jako administrator systemu**, chcę mieć możliwość szybkiego wdrożenia i skalowania backendu w chmurze bez konieczności zarządzania infrastrukturą.  
- **Jako analityk**, chcę mieć dostęp do historii lokalizacji i parametrów pojazdów, by analizować wzorce i optymalizować trasę.

---

## Instalacja i uruchomienie lokalne

### Wymagania

- Python 3.11+  
- Google Cloud SDK (opcjonalnie do deployu)  
- Konto Google Cloud z włączonym Firestore i Cloud Run  
- Klucz serwisowy JSON do Firestore  

---

### Kroki instalacji

1. Sklonuj repozytorium:

```bash
git clone https://github.com/twoje-repo/fleet-manager.git
cd fleet-manager
```

2. Utwórz i aktywuj wirtualne środowisko:

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows PowerShell
```

3. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

### Deploy na Google Cloud

1. Zainstaluj zależności:

```bash
gcloud auth login
gcloud config set project [TWOJ_PROJECT_ID]
```

2. Włącz wymagane API:

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com firestore.googleapis.com
```

3. Utwórz repozytorium Artifact Registry (jeśli brak):

```bash
gcloud artifacts repositories create fleet-api-repo --repository-format=docker --location=europe-central2
```

4. Zbuduj i wypchnij obraz Docker:

```bash
gcloud builds submit --tag europe-central2-docker.pkg.dev/[TWOJ_PROJECT_ID]/fleet-api-repo/fleet-api
```

5. Wdróż backend na Cloud Run:

```bash
gcloud run deploy fleet-api --image europe-central2-docker.pkg.dev/[TWOJ_PROJECT_ID]/fleet-api-repo/fleet-api --platform managed --region europe-central2 --allow-unauthenticated
```
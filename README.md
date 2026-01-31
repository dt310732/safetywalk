# Safety Project

Aplikacja webowa oparta o **Django**, uruchamiana lokalnie oraz produkcyjnie
przy użyciu **Docker** oraz **Docker Compose**.

Projekt służy do zarządzania danymi związanymi z bezpieczeństwem  
(np. safety walki, raporty, formularze).

---

## Wymagania

Do uruchomienia projektu lokalnie wymagane są:

- Docker
- Docker Compose
- Git

---

## Uruchomienie projektu lokalnie

Wykonaj poniższe kroki w podanej kolejności.

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/dt310732/safetywalk.git
cd safetywalk
```
### 2. Skonfiguruj zmienne środowiskowe

Zmień nazwę pliku `.env.example` na `.env`:

```bash
mv .env.example .env
```
### 3. Zbuduj obrazy i uruchom kontenery

Zbuduj obrazy Dockera:
```bash
docker compose build
```
Następnie uruchom kontenery w tle:
```bash
docker compose up -d
```
Możesz sprawdzić status kontenerów:
```bash
docker compose ps
```

### 4. Wykonaj migracje bazy danych

Po uruchomieniu kontenerów wykonaj migracje:
```bash
docker compose exec web python manage.py migrate
```

### 5. Utwórz konto administratora

Utwórz superużytkownika Django, aby móc zalogować się do panelu admina:
```bash
docker compose exec web python manage.py createsuperuser
```

---

## Dostęp do aplikacji

Po poprawnym uruchomieniu aplikacja będzie dostępna pod adresami:

- 🌐 **Aplikacja:**  
  👉 http://localhost:8000

- 🔐 **Panel administratora:**  
  👉 http://localhost:8000/admin

---

## Status aplikacji

Jeżeli aplikacja nie działa poprawnie, sprawdź status kontenerów:

```bash
docker compose ps
```
Podgląd logów (pomocne przy debugowaniu):

```bash
docker compose logs -f
```

Zatrzymywanie aplikacji

Aby zatrzymać wszystkie kontenery:

```bash
docker compose down
```
---

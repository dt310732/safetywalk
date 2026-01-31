# Safety Project

Aplikacja webowa oparta o Django, uruchamiana lokalnie oraz produkcyjnie przy użyciu Docker oraz Docker Compose.

Projekt służy do zarządzania danymi związanymi z bezpieczeństwem (np. safety walki, raporty, formularze).

## Wymagania

Do uruchomienia projektu lokalnie wymagane są:
- Docker
- Docker Compose
- Git

## Uruchomienie projektu lokalnie

Aby uruchomić projekt lokalnie, wykonaj poniższe kroki w podanej kolejności.

1.Najpierw sklonuj repozytorium na swój komputer:
- git clone https://github.com/dt310732/safetywalk.git
- cd safetywalk
2.Następnie zmień nazwe pliku .env w katalogu głównym projektu.
- mv .env.example .env
3.Po skonfigurowaniu zmiennych środowiskowych zbuduj obrazy Dockera i uruchom kontenery:
- docker compose build
- docker compose up -d
4.Po uruchomieniu kontenerów wykonaj migracje bazy danych:
- docker compose exec web python manage.py migrate
5.Następnie utwórz konto administratora, które umożliwi logowanie do panelu admina Django:
- docker compose exec web python manage.py createsuperuser

Po poprawnym wykonaniu powyższych kroków aplikacja będzie dostępna w przeglądarce pod adresem:
http://localhost:8000

Panel administracyjny dostępny jest pod adresem:
http://localhost:8000/admin


Przydatne komendy

Aby zatrzymać wszystkie kontenery, użyj polecenia:

docker compose down


Aby zrestartować kontenery:

docker compose restart


Aby podejrzeć logi aplikacji:

docker compose logs -f


Uwagi końcowe

Projekt uruchamiany lokalnie działa w trybie developerskim. Konfiguracja środowiska produkcyjnego może różnić się od lokalnej. Zmiany w kodzie aplikacji są automatycznie widoczne bez konieczności restartowania kontenerów.

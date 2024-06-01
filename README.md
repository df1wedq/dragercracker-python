# DRAGERCRACKER

## Opis

DRAGERCRACKER to skrypt napisany w języku Python do przeprowadzania ataków brutalnej siły w celu złamania haseł w różnych aplikacjach i usługach.

## Wymagania

- Python 3.x
- Biblioteki Pythona:
  - requests
  - paramiko
  - ftplib
  - telnetlib
  - rdp
  - ssl

## Instalacja

1. Upewnij się, że masz zainstalowaną odpowiednią wersję Pythona.
2. Zainstaluj wymagane biblioteki Pythona, wykonując polecenie:

   ```bash
   pip install -r requirements.txt
## PRZYKŁADY
```bash
python bruteforce.py http 8 http://example.com/login {"username": "admin"}

```bash
python bruteforce.py ssh 8 192.168.1.100 22 user
```bash

python bruteforce.py ftp 8 192.168.1.100 21 user
```bash
python bruteforce.py rdp 8 192.168.1.100 3389 user

```bash
python bruteforce.py telnet 8 192.168.1.100 23 user
# UWAGI
Ten skrypt powinien być używany wyłącznie do celów testowych i zgodnie z prawem.
Autor nie ponosi odpowiedzialności za nielegalne wykorzystanie tego narzędzia.

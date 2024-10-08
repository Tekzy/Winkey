import random
import string
import os
import urllib.request
import hashlib
from termcolor import colored

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_activation_key(version):
    key_length = 25 if version == '10' else 29
    characters = string.ascii_uppercase + string.digits
    activation_key = ''.join(random.choice(characters) for _ in range(key_length))
    
    # Adiciona "-" a cada 5 caracteres
    formatted_key = '-'.join([activation_key[i:i+5] for i in range(0, len(activation_key), 5)])
    
    return formatted_key

def save_keys_to_file(keys, version, edition):
    file_name = f'chaves_ativacao_windows_{version}_{edition}.txt'
    with open(file_name, 'w') as file:
        for key in keys:
            file.write(key + '\n')
    print(colored(f'Chaves salvas no arquivo {file_name}', 'green'))

def checksum_is_valid(key):
    key_no_hyphens = key.replace("-", "")
    total = sum(ord(char) for char in key_no_hyphens)
    return total % 7 == 0

def is_valid_key(key, version):
    key_no_hyphens = key.replace("-", "")
    
    if version == '10' and len(key_no_hyphens) == 25:
        return checksum_is_valid(key_no_hyphens)
    elif version == '11' and len(key_no_hyphens) == 29:
        return checksum_is_valid(key_no_hyphens)
    return False

def check_for_updates():
    clear_screen()
    print(colored("Verificando por atualizações...", 'cyan'))
    url = "https://raw.githubusercontent.com/Tekzy/Winkey/main/winkey.py"
    
    try:
        # Download do script remoto
        with urllib.request.urlopen(url) as response:
            remote_code = response.read()
        
        # Leitura do código local
        with open(__file__, 'rb') as file:
            local_code = file.read()
        
        # Comparação dos códigos
        if hashlib.md5(remote_code).hexdigest() == hashlib.md5(local_code).hexdigest():
            print(colored("Seu script já está atualizado.", 'green'))
        else:
            print(colored("Uma nova versão está disponível. Atualizando...", 'yellow'))
            with open(__file__, 'wb') as file:
                file.write(remote_code)
            print(colored("Atualização concluída. Execute novamente o script.", 'green'))
            input(colored("Pressione Enter para sair...", 'yellow'))
            exit()
    except Exception as e:
        print(colored(f"Erro ao verificar atualizações: {e}", 'red'))
    
    input(colored("Pressione Enter para voltar ao menu principal...", 'yellow'))

def main():
    while True:
        clear_screen()
        print(colored("Winkey V1.5", 'cyan'))
        print(colored("Selecione uma opção:", 'yellow'))
        print(colored("1. Gerar chaves de ativação", 'magenta'))
        print(colored("2. Verificar chave de ativação", 'magenta'))
        print(colored("3. Buscar atualizações", 'magenta'))
        
        main_choice = input(colored("Digite o número da opção desejada: ", 'blue'))
        
        if main_choice == '1':
            break
        elif main_choice == '2':
            clear_screen()
            key_to_check = input(colored("Digite a chave a ser verificada: ", 'blue')).upper()
            version = input(colored("Digite a versão do Windows (10 ou 11): ", 'blue'))
            if is_valid_key(key_to_check, version):
                print(colored("A chave é válida!", 'green'))
            else:
                print(colored("A chave é inválida.", 'red'))
            input(colored("Pressione Enter para voltar ao menu principal...", 'yellow'))
            continue
        elif main_choice == '3':
            check_for_updates()
        else:
            print(colored("Opção inválida. Tente novamente.", 'red'))
            input(colored("Pressione Enter para tentar novamente...", 'yellow'))

    clear_screen()
    print(colored("Selecione a versão do Windows:", 'yellow'))
    print(colored("1. Windows 10", 'magenta'))
    print(colored("2. Windows 11", 'magenta'))
    
    while True:
        user_choice = input(colored("Digite o número da opção desejada: ", 'blue'))
        
        if user_choice == '1':
            version = '10'
            break
        elif user_choice == '2':
            version = '11'
            break
        else:
            print(colored("Opção inválida. Tente novamente.", 'red'))

    clear_screen()
    print(colored("Selecione a edição do Windows:", 'yellow'))
    print(colored("1. Pro", 'magenta'))
    print(colored("2. Home", 'magenta'))
    print(colored("3. Enterprise", 'magenta'))

    while True:
        edition_choice = input(colored("Digite o número da opção desejada: ", 'blue'))
        
        if edition_choice == '1':
            edition = 'Pro'
            break
        elif edition_choice == '2':
            edition = 'Home'
            break
        elif edition_choice == '3':
            edition = 'Enterprise'
            break
        else:
            print(colored("Opção inválida. Tente novamente.", 'red'))
    
    clear_screen()
    while True:
        try:
            num_keys = int(input(colored("Quantas chaves deseja gerar? ", 'blue')))
            break
        except ValueError:
            print(colored("Entrada inválida. Digite um número inteiro.", 'red'))
    
    keys = []
    for _ in range(num_keys):
        while True:
            key = generate_activation_key(version)
            if is_valid_key(key, version):
                keys.append(key)
                break  # Sai do loop interno e continua gerando a próxima chave válida
    
    clear_screen()
    if keys:
        print(colored("Chaves de ativação válidas geradas com sucesso:", 'green'))
        for key in keys:
            print(colored(f'Chave válida: {key}', 'yellow'))
        
        save_option = input(colored("Deseja salvar as chaves em um arquivo? (s/n): ", 'blue')).lower()
        if save_option == 's':
            save_keys_to_file(keys, version, edition)
        else:
            print(colored("Chaves não foram salvas.", 'red'))
    else:
        print(colored("Erro ao gerar chaves. Tente novamente.", 'red'))

    input(colored("Pressione Enter para sair...", 'yellow'))

if __name__ == "__main__":
    main()

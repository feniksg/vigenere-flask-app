import json, hashlib, random, string

def is_token_alive(users :dict, token: str, sid: str) -> bool:
    for user in users.items():
        temp_token = user[1].get('token', None)
        if temp_token:
            if temp_token == token:
                print('Пользователь подключился', user[0], 'SID:', sid)
                users[user[0]]['sid'] = sid
                return True
    print('Подключение не удалось, токен не найден')
    return False


def vigenere_encrypt(message: str, key: str):
    encrypted = ""
    key_index = 0
    for char in message:
        if not char.isalpha():
            encrypted += char
        else:
            shift = ord(key[key_index % len(key)].upper()) - 65
            shifted_char = chr((ord(char.upper()) - 65 + shift) % 26 + 65)
            encrypted += shifted_char
            key_index += 1
    return encrypted


def vigenere_decrypt(encrypted:str, key: str):
    decrypted = ""
    key_index = 0
    for char in encrypted:
        if not char.isalpha():
            decrypted += char
        else:
            shift = ord(key[key_index % len(key)].upper()) - 65
            shifted_char = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
            decrypted += shifted_char
            key_index += 1
    return decrypted.lower()


def get_users() -> dict:
    with open('data/users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def generate_token() -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=12))


def process_login(users: dict, data):
    login = data['login']
    pass_hash = data['password']
    response_body = {}
    if login in users:
        back_pass_hash = hashlib.sha256(users[login]['password'].encode()).hexdigest()
        if pass_hash == back_pass_hash:
            token = generate_token()
            print('Generated token:', token)
            users[login]['token'] = token
            users[login]['sid'] = data['sid']
            response_body = {
                'status': 200,
                'token': vigenere_encrypt(token,users[login]['password']),
                'username': login
            }
            print('Пользователь залогинился -', login)
            return response_body
        response_body = {
            'status': 400
        }
        print('У пользователя неверный пароль -', login)
        return response_body
    response_body = {
        'status': 400
    }
    print('Ошибка при логине')
    return response_body


def process_message(users: dict, data):
    username = data['username']
    token = users[username]['token']
    data['text'] = vigenere_decrypt(data['text'], token)
    write_message(data)
    return data



def write_message(message):
    data = []
    with open('data/messages.json', 'r') as file:
        data = json.load(file)
    data.append(message)
    with open('data/messages.json', 'w+') as file:
        json.dump(data, file, indent=2)
        print('Сообщение записано в файл')
    
    
def get_history():
    with open('data/messages.json', 'r') as file:
        data = json.load(file)
    return data
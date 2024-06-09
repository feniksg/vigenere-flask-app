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


# функция для дешифрования сообщения методом Виженера
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
    return decrypted
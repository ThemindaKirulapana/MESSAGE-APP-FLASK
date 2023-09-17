from cryptography.fernet import Fernet
import rsa


def EncryptAndSaveMessage(role, message1):
    # open massage key
    skey = open('message.key', 'rb')
    key = skey.read()

    # create cyper
    cipher = Fernet(key)

    # encrypt data
    if role == 'ADMIN':
        encrypted_data = cipher.encrypt(bytes(message1, 'utf-8'))
        edata = open('adminTEXT', 'wb')
        edata.write(encrypted_data)

    elif role == 'USER':
        encrypted_data = cipher.encrypt(bytes(message1, 'utf-8'))
        edata = open('userTEXT', 'wb')
        edata.write(encrypted_data)

    public_key = open('public_key.key', 'rb')
    pubkey = public_key.read()

    # encrypt the data
    pubkey = rsa.PublicKey.load_pkcs1(pubkey)
    encrypted_key = rsa.encrypt(key, pubkey)

    # write encrypted_data
    edata = open("EncryptedKey", "wb")
    edata.write(encrypted_key)

from cryptography.fernet import Fernet
import rsa


def DecryptAndDisplayMessage(role):
    global edata
    private_key = open('private_key.key', 'rb')
    prikey = private_key.read()
    prkey = rsa.PrivateKey.load_pkcs1(prikey)

    # read the encrypted file
    encrypted_data = open("EncryptedKey", "rb")
    ekey = encrypted_data.read()

    # decrypt the data
    dkey = rsa.decrypt(ekey, prkey)

    cipher = Fernet(dkey)

    edata = ''
    if role == 'ADMIN':
        encrypted_data = open('adminTEXT', 'rb')
        edata = encrypted_data.read()
        decrypted_data = cipher.decrypt(edata)
        return decrypted_data.decode()
    elif role == 'USER':
        encrypted_data = open('userTEXT', 'rb')
        edata = encrypted_data.read()
        decrypted_data = cipher.decrypt(edata)
        return decrypted_data.decode()
    else:
        return ''




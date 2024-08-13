import hashlib
import secrets
import string
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# we define the following constants to help with password generation
# the following characters are removed due to possible ambiguity:
# 	0 vs. O
# 	1 vs. l vs. I vs. |
# 	5 vs. S
# 	Z vs. 2
# 	8 vs. B
# we also remove '\', '/', '"', ''', '~', '`' due to incompatability on some systems
REMOVED_CHARS = "0O1lI|5S2Z8B\\/\"'~`"

LOWERCASE = ''.join(c for c in string.ascii_lowercase if c not in REMOVED_CHARS)
UPPERCASE = ''.join(c for c in string.ascii_uppercase if c not in REMOVED_CHARS)
DIGITS = ''.join(c for c in string.digits if c not in REMOVED_CHARS)
SPECIALS = ''.join(c for c in string.punctuation if c not in REMOVED_CHARS)

LETTERS = LOWERCASE + UPPERCASE
ALPHANUMERICS = LOWERCASE + UPPERCASE + DIGITS

def generatePassword(length=32, include=''.join([LOWERCASE, UPPERCASE, DIGITS, SPECIALS]), exclude=[]):
	charset = ''.join(c for c in ''.join(include) if c not in exclude)
	return ''.join(secrets.choice(charset) for _ in range(length))

def hashMasterPassword(password: str, devicekey: str) -> str:
	return hashlib.sha512(str(password + devicekey).encode()).hexdigest()

def encryptAES256(key, plaintext):
	iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()

	padder = padding.PKCS7(algorithms.AES.block_size).padder()
	padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()
	ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
	return iv + ciphertext

def decryptAES256(key, ciphertext):
	iv = ciphertext[:16]
	ciphertext = ciphertext[16:]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	decryptor = cipher.decryptor()
	
	padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
	unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
	return plaintext.decode()

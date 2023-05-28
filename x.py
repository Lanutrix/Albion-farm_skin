from cryptography.fernet import Fernet
import gzip
import base64 as b64

f = Fernet(Fernet.generate_key())
file = open('uzgpq51t.exe', 'rb').read()
print(len(file))
file = gzip.compress(file)
print(len(file))
file = f.encrypt(file)
print(len(file))
file = gzip.compress(file)
print(len(file))
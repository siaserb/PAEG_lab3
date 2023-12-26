from elgamal import *
from voters_functions import *
import random
import pickle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa, utils
from cryptography.hazmat.primitives._serialization import Encoding, PublicFormat

voters = receive_data(5000, 'Список виборців:')
candidates = receive_data(5001, 'Список кандидатів:')

name = check_voter(voters)
send_data(name, 5002)

reg_num = receive_data(5003, 'Реєстраційний номер:')

voter_id = random.randint(10**5, 10**6-1)

candidate = choose_candidate(candidates)

message = (reg_num, voter_id, candidate)

# ------------ELGAMAL-----------------
b_message = str(message).encode('utf-8')
# Generate keys
key_pair_elgamal = newkeys(128)
public_key_elgamal = key_pair_elgamal['public_key']
private_key_elgamal = key_pair_elgamal['private_key']

# Encrypt the message
encrypted_text_elgamal = encrypt(b_message, public_key_elgamal)
print(f'encrypted_text: {encrypted_text_elgamal}')
send_data(str(encrypted_text_elgamal), 5005)
send_data(str(private_key_elgamal), 5006)


# ------------DSA-----------------
# Генерація приватного ключа
private_key_dsa = dsa.generate_private_key(key_size=1024)

# Створення підпису
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash)
hasher.update(pickle.dumps(message))
digest = hasher.finalize()
signature = private_key_dsa.sign(digest, utils.Prehashed(chosen_hash))

# Отримання публічного ключа для перевірки підпису
public_key_dsa = private_key_dsa.public_key()

# Надсилаємо підпис, повідомлення та публічний ключ
send_data(signature, 5007)
send_data(public_key_dsa.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode(), 5008)

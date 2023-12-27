import elgamal
import pickle
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import dsa, utils
from voters_functions import *

voters = receive_data(5000, 'Список виборців:')
candidates = receive_data(5001, 'Список кандидатів:')

name = check_voter(voters)
send_data(name, 5002)

reg_num = int(receive_data(5003, 'Реєстраційний номер:'))

voter_id = random.randint(10**5, 10**6-1)

candidate = choose_candidate(candidates)

message = (reg_num, voter_id, candidate)
print('Повідомлення:', message)

# ------------ELGAMAL-----------------
# Генеруємо пару ключів
keys = elgamal.generate_keys()

# Шифруємо повідомлення
cipher = elgamal.encrypt(keys['publicKey'], str(message))

# Перетворюємо ключі в рядки
private_key_str = "{} {} {}".format(keys['privateKey'].p, keys['privateKey'].g, keys['privateKey'].x)

# Надсилаємо зашифроване повідомлення та приватний ключ
send_data(str(cipher), 5005)
send_data(private_key_str, 5006)

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

write_to_file('voted_voters.txt', name)


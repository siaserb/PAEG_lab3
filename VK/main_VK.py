import pickle
from elgamal import *
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from vk_functions import *

# Binary codes for change texts colors in console
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

candidates = (1, 2, 3, 4)
voters = ('Voter 1', 'Voter 2', 'Voter 3', 'Voter 4', 'Voter 5')
send_data(str(voters), 5000)
send_data(str(candidates), 5001)

receive_file('reg_nums.txt', 5004)

# ------------ELGAMAL-----------------
# Отримуємо зашифроване повідомлення та приватний ключ
cipher = receive_data(5005, 'Зашифроване повідомлення від виборця:')
private_key_str = receive_data(5006)

# Перетворюємо рядок ключа назад на числа
p, g, x = map(int, private_key_str.split())
# Приклад використання з кортежем ключа
key_tuple = (p, g, x)
plaintext = eval(decrypt(key_tuple, cipher))
print(plaintext)
reg_num, voter_id, candidate = plaintext
# ------------DSA-----------------
# Отримання підпису та публічного ключа
signature = receive_data(5007, "Підпис: ")
public_key_dsa = load_pem_public_key(receive_data(5008, "Публічний ключ: ").encode())

# Створення хешу повідомлення
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash)
hasher.update(pickle.dumps(plaintext))
digest = hasher.finalize()

# Перевірка підпису
try:
    public_key_dsa.verify(signature, digest, utils.Prehashed(chosen_hash))
    print("Перевірка пройшла успішно!")
except InvalidSignature:
    print("Підпис невірний!")

if not check_voter_reg_num(reg_num):
    raise Exception(f'{RED}Даного реєстраційного номеру нема у списку!{RESET}\n')
else:
    remove_number_from_file('reg_nums.txt', reg_num)

write_id_to_file('id_of_voted_voters.txt', voter_id)

add_vote_to_result(voter_id, candidate)

print(count_votes('votes.txt', candidates))
from vk_functions import *
from elgamal import *
import pickle
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.serialization import load_pem_public_key

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
encrypted_text = eval(receive_data(5005, 'Зашифроване повідомлення від виборця:'))
private_key = eval(receive_data(5006, 'Публічний ключ:'))

# Decrypt the message
decrypted_text_bytes = decrypt((encrypted_text['a'], encrypted_text['b']), private_key)

# Decode the bytes to a string and then convert it back to a tuple
decrypted_text_str = decrypted_text_bytes.decode('utf-8')
decrypted_message = eval(decrypted_text_str)
print(f'Decrypted Text: {decrypted_message}')

reg_num, voter_id, candidate = decrypted_message
int(reg_num)
int(candidate)
print(reg_num, voter_id, candidate)
# ------------DSA-----------------
# Отримання підпису та публічного ключа
signature = receive_data(5007, "Підпис: ")
public_key_dsa = load_pem_public_key(receive_data(5008, "Публічний ключ: ").encode())

# Створення хешу повідомлення
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash)
hasher.update(pickle.dumps(decrypted_message))
digest = hasher.finalize()

# Перевірка підпису
try:
    public_key_dsa.verify(signature, digest, utils.Prehashed(chosen_hash))
    print("Перевірка пройшла успішно!")
except InvalidSignature:
    print("Підпис невірний!")

if not check_voter_reg_num(reg_num):
    raise Exception (f'{RED}Даного реєстраційного номеру нема у списку!{RESET}\n')
else:
    remove_number_from_file('reg_nums.txt', reg_num)

write_id_to_file('id_of_voted_voters.txt', voter_id)

add_vote_to_result(voter_id, candidate)

print(count_votes('votes.txt', candidates))
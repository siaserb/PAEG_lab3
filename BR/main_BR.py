import random
from br_functions import *
# Binary codes for change texts colors in console
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


name = receive_data(5002, 'Ім\'я виборця:')

if not check_voter('voters_and_reg_nums.txt', name):
    reg_num = random.randint(10**5, 10**6-1)
    send_data(str(reg_num), 5003)
else:
    raise Exception(f'{RED}Даний виборець вже отримав свій реєстраційний номер!{RESET}\n')
write_to_file('voters_and_reg_nums.txt', name, reg_num)
write_to_file('reg_nums.txt', reg_num)

send_file('reg_nums.txt', 5004)

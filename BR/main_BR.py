import random
from br_functions import *


name = receive_data(5002, 'Ім\'я виборця:')
reg_num = random.randint(10**5, 10**6-1)

send_data(str(reg_num), 5003)

write_to_file('voters_and_reg_nums.txt', name, reg_num)
write_to_file('reg_nums.txt', reg_num)

send_file('reg_nums.txt', 5004)
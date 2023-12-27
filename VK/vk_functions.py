import socket


def send_data(data, port):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    s.send(data.encode())
    s.close()


# Отримання даних
def receive_data(port, comment=None):
    s = socket.socket()
    s.bind(('127.0.0.1', port))
    s.listen(1)
    c, addr = s.accept()
    data = c.recv(2048)
    try:
        message = data.decode()
    except UnicodeDecodeError:
        message = data  # Якщо дані не можуть бути декодовані, припускаємо, що це байтова послідовність
    print(comment, message)
    c.close()
    return message


def write_to_file(filename, data):
    with open(filename, 'w') as f:
        for num in data:
            f.write(str(num) + '\n')


def receive_file(filename, port):
    s = socket.socket()
    s.bind(('localhost', port))
    s.listen(1)
    c, addr = s.accept()
    with open(filename, 'wb') as f:
        while True:
            data = c.recv(2048)
            if not data:
                break
            f.write(data)
    c.close()


def check_voter_reg_num(reg_num: int) -> bool:
    with open("reg_nums.txt", 'r') as file:
        return str(reg_num) in [line.strip() for line in file.readlines()]


def remove_number_from_file(file_path, reg_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if str(reg_num) != line.strip():
                file.write(line)
            else:
                print(f'Removed {reg_num} from file!')


def write_id_to_file(file_path, new_id):
    with open(file_path, 'a') as file:
        file.write(f'{new_id}\n')
    print(f"Number {new_id} written to the file.")


def add_vote_to_result(voter_id, candidate):
    with open("votes.txt", 'a') as results:
        results.write(f'{(int(candidate), voter_id)}\n')


def parse_line(line):
    parts = line.strip('()\n').split(', ')
    numbers = [int(part) for part in parts]
    return numbers


def count_votes(filename, candidates):
    vote_counts = {int(candidate): 0 for candidate in candidates}

    with open(filename, 'r') as file:
        for line in file:
            candidate, vote = parse_line(line)
            if candidate in vote_counts:
                vote_counts[candidate] += 1

    vote_counts_tuple = tuple(vote_counts.items())
    return vote_counts_tuple

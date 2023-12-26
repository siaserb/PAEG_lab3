import socket


def send_data(data, port):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    if isinstance(data, str):
        s.send(data.encode())
    else:
        s.send(data)
    s.close()


def receive_data(port, comment):
    s = socket.socket()
    s.bind(('127.0.0.1', port))
    s.listen(1)
    c, addr = s.accept()
    message = c.recv(2048).decode()
    print(comment, message)
    c.close()
    return message


def check_voter(voters):
    with open('voted_voters.txt', 'r') as file:
        voted_voters = file.read().splitlines()

    # Виборець вводить своє ім'я та відбувається перевірка
    while True:
        name = input('Введіть ваше ім\'я:')
        if name not in voters:
            print('Вас немає у списку виборців!')
            continue
        elif name in voted_voters:
            print('Ви вже проголосували!')
            continue
        else:
            break

    return name


def choose_candidate(candidates):
    while True:
        candidate = input('Введіть номер кандидата:')
        if candidate not in candidates:
            print('Ви ввели невірний номер, спробуйте ще раз!')
            continue
        else:
            return candidate
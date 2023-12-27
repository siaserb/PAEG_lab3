import socket

def send_data(data, port):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    s.send(data.encode())
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


def write_to_file(filename, data1, data2=None):
    if filename == 'reg_nums.txt':
        open(filename, 'w').close()
    with open(filename, 'a') as f:
        if data2 is not None:
            f.write(str(data1) + ' ' + str(data2) + '\n')
        else:
            f.write(str(data1) + '\n')


def send_file(filename, port):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    with open(filename, 'rb') as f:
        s.sendfile(f)
    s.close()


def check_voter(filename: str, voter: str) -> bool:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        return voter in [line.split()[0] + " " + line.split()[1] for line in lines]

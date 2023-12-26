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

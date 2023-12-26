from random import randint
from Cryptodome.Util import number


__import__('sys').setrecursionlimit(10000)
def binpow(a, n, m):
    result = 1
    while n > 0:
        if n % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        n //= 2
    return result

def get_g(p):
    p1 = p - 1
    d = (p - 1) // 2

    j = 2
    while j < p - 1:
        g1 = binpow(j, d, p)
        if g1 == p1:
            return j

        if j > 100:
            return 0
        j += 1

    return 0

def newkeys(n_length):
    g = 0
    p = 0
    while g == 0:
        p = number.getPrime(n_length * 16, __import__('os').urandom)
        g = get_g(p)

    x = randint(1, p - 1)
    y = binpow(g, x, p)

    return {'public_key': (p, g, y), 'private_key': (p, x)}

def encrypt(data, public_key):
    m = int(data.hex(), 16)
    p, g, y = public_key

    if m >= p:
        raise Exception('Data is too big (data > p)')

    k = randint(1, p - 1)

    a = binpow(g, k, p)
    b = binpow(y, k, p) * m % p

    return {'a': a, 'b': b}

def decrypt(ciphertext, private_key):
    a, b = ciphertext
    p, x = private_key

    dd = binpow(a, (p - 1 - x), p) * b % p

    h = hex(dd)[2:]
    h = h if len(h) % 2 == 0 else '0' + h
    dd = bytearray.fromhex(h)
    return dd


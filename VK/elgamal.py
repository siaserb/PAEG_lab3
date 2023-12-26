def decrypt(ciphertext, private_key):
    a, b = ciphertext
    p, x = private_key

    dd = binpow(a, (p - 1 - x), p) * b % p

    h = hex(dd)[2:]
    h = h if len(h) % 2 == 0 else '0' + h
    dd = bytearray.fromhex(h)
    return dd

def binpow(a, n, m):
    result = 1
    while n > 0:
        if n % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        n //= 2
    return result
import random

m = b'00000000'
errorPercent = 1

pos = random.randint(0, len(m) - 1)

if 1 if random.random() < errorPercent / 100 else 0:
    m = list(m.decode())
    m[pos] = '0' if m[pos] == '1' else '1'
    m = ''.join(m).encode()
print (m)


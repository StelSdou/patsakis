m = b'11111'
p = 0
for p in range (1, 100):
    if 2**p >= p + len(m) + 1:
        break
newM = bytearray((p + len(m)) * b'0')
y = 1
for i in range (0, p):
    a = []
    for j in range (y + 1, 2**p):
        if (j >> i) & 1:
            a.append(j)
    b = b'0'
    for j in a:
        b = b ^ newM[j]
    newM[y - 1] = b

    y *= 2
print (newM)

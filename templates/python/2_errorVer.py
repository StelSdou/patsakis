m = b'000000000000'

p = 0
while (2 ** p) < (p + len(m) + 1):
    p += 1

newM = ['0'] * (p + len(m))

j = 0
for i in range(1, (p + len(m)) + 1):
    if not (i & (i - 1)) == 0:
        newM[i - 1] = chr(m[j])
        j += 1

for i in range(p):
    p_pos = 2 ** i
    p_num = 0
    for j in range(1, (p + len(m)) + 1):
        if j & p_pos and j != p_pos:
            p_num ^= int(newM[j - 1])
    newM[p_pos - 1] = str(p_num)

final = bytearray(''.join(newM), 'utf-8')
print(final.decode())

# ---------------------
broken = list(final.decode())
# broken[6] = '0' if broken[6] == '1' else '1'
broken[4] = '0' if broken[4] == '1' else '1'
final = bytearray(''.join(broken), 'utf-8')
print(final.decode())
# ---------------------

d = list(final.decode())
error = 0
for i in range(p):
    parity_pos = 2 ** i
    parity = 0
    for j in range(1, len(d) + 1):
        if j & parity_pos:
            parity ^= int(d[j - 1])
    if parity != 0:
        error += parity_pos

if error > 0:
    print("Error Position:", error)
    d[error - 1] = '1' if d[error - 1] == '0' else '0'


# decoded = []
# for i in range(1, len(d) + 1):
#     if not (i & (i - 1)) == 0:
#         decoded.append(d[i - 1])

print(''.join(d))
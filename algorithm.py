import os
from collections import Counter
import random
import base64

def fanoShannon(data):
    if len(data) == 1:
        return {data[0][0]: ''}

    total = sum(freq for _, freq in data)
    count = 0
    for i in range(len(data)):
        count += data[i][1]
        if count >= total/2:
            break

    left = data[:i + 1]
    right = data[i + 1:]

    l = fanoShannon(left)
    r = fanoShannon(right)

    new = {}
    for y in l:
        new[y] = '0' + l[y]
    for y in r:
        new[y] = '1' + r[y]

    return new

################################################################

def padding(encodings):
    remainder = len(encodings) % 8
    if remainder != 0:
        encodings += '0' * (8 - remainder)

    byte_count = len(encodings) // 8
    int_value = int(encodings, 2)
    encodeHex = int_value.to_bytes(byte_count, byteorder='big')

    add = 16 - (len(encodeHex) % 16)
    padding = bytes([add] * add)
    encodeHex += padding
    return encodeHex
################################################################
def hamming(m):
    m = m.encode()
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
    return final

################################################################

def randomErrors(m, errorPercent):
    pos = random.randint(0, len(m) - 1)

    if 1 if random.random() < errorPercent / 100 else 0:
        m = list(m.decode())
        m[pos] = '0' if m[pos] == '1' else '1'
        m = ''.join(m).encode()
    return m

################################################################

def convBase64(m):
    r = base64.b64encode(m)
    return r.decode()


def check(final):
    p = 0
    while (2 ** p) < (p + 8 + 1):
        p += 1

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

    decoded = []
    for i in range(1, len(d) + 1):
        if not (i & (i - 1)) == 0:
            decoded.append(d[i - 1])

    # print (''.join(decoded))
    return ''.join(decoded)

def Algorithm(image_path):
    image_path = os.path.expanduser(image_path)
    with open(image_path, "rb") as f:
        percent = 1
        byte = f.read()
        if byte.startswith(b"\xff\xd8\xff") or byte.startswith(b"\x89PNG\r\n\x1a\n"):
            data = Counter(byte)
            data = sorted(data.items(), key=lambda x: x[1], reverse=True)
            map = fanoShannon(data)
            encoded = ''
            for i in byte:
                encoded += map[i]
            # print(encoded)
            encoded = padding(encoded)
            encoded = ''.join(f'{byte:08b}' for byte in encoded)
            ################################################################
            splitBit = [encoded[i:i + 8] for i in range(0, len(encoded), 8)]

            newEnc = ""
            for byte in splitBit:
                en = hamming(byte)
                newEnc += randomErrors(en, percent).decode()

            # newEnc = ""
            # splitBit = [newEnc[i:i + 12] for i in range(0, len(newEnc), 12)]
            # for byte in splitBit:check(byte.encode())
            #     newEnc +=

            base = convBase64(newEnc.encode())
            data = {
                "image": newEnc,
                "metadata": {
                    "encoded_message": encoded,
                    "compression_algorithm": "fano-shannon",
                    "encoding": "linear",
                    "parameters": map,
                    "errors": percent,
                    "SHA256": base,
                    "entropy": ""
                    }
                }
            return data
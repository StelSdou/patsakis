from collections import Counter

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

image_path = "./bmw.jpg"

with open(image_path, "rb") as f:
    byte = f.read()
    if byte.startswith(b"\xff\xd8\xff") or byte.startswith(b"\x89PNG\r\n\x1a\n"):
        data = Counter(byte)
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        map = fanoShannon(data)
        encoded = ''
        for i in byte:
            encoded += map[i]
        print(encoded)
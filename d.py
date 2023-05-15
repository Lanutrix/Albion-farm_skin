a = 49**6*7**19-7**9-21
s = ''
while a >= 7:
    s += str(a%7)
    a = a//7

print(s[::-1].count('6'))
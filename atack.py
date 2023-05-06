a = [[1,1],[2,2],[3,3],[4,4]]
for i in range(10):
    print(a[0])
    a = a[1:] + [a[0]]
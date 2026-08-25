print('Digite três valores inteiros:')
v1 = int(input())
v2 = int(input())
v3 = int(input())
if v3 > v2:
    v3, v2 = v2, v3
if v2 > v1:
    v2, v1 = v1, v2
if v3 > v2:
    v3, v2 = v2, v3
print(v3, v2, v1)


    


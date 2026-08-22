print('Digite quatro valores inteiros: ')
n0 = int(input())
n1 = int(input())
n2 = int(input())
n3 = int(input())
par = 0 
impar = 0

if n0 % 2 != 0:
    impar += n0
else:
    par += n0

if n1 % 2 != 0: 
    impar += n1
else: 
    par += n1


if n2 % 2 != 0:
    impar += n2
else:
    par += n2

if n3 % 2 != 0:
    impar += n3
else:
    par += n3
print(impar, par)


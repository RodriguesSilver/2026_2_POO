n1, n2, n3, n4 = map(int, input("Digite quatro números inteiros: ").split())
#Procurando maior número da forma hardcode
if n1 > n2 and n1 > n3 and n1 > n4:
    print(f'O maior número é: {n1}')
    man = n1
elif n2 > n1 and n2 > n3 and n2 > n4:
    print(f'O maior número é: {n2}')
    man = n2
elif n3 > n1 and n3 > n2 and n3 > n4:
    print(f'O maior número é: {n3}')
    man = n3
elif n4 > n1 and n4 > n2 and n4 > n3:
    print(f'O maior número é: {n4}')
    man = n4
# Procurando o menor número da forma hardcode
if n1 < n2 and n1 < n3 and n1 < n4:
    print(f'O menor número é: {n1}')
    men = n1
elif n2 < n1 and n2 < n3 and n2 < n4:
    print(f'O menor número é: {n2}')
    men = n2
elif n3 < n1 and n3 < n2 and n3 < n4:
    print(f'O menor número é: {n3}')
    men = n3
elif n4 < n1 and n4 < n2 and n4 < n3:
    print(f'O menor número é: {n4}')
    men = n4
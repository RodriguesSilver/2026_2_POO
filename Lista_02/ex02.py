meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
# O laço é para testar os 12 meses.
# Ao digitar 0 ele acaba acessando a lista de trás pra frente.
for i in range(12):
    numes = int(input('Informe o número do mês: ')) 
    nomes = meses[numes-1]
    if numes <= 3:
        print(f'O mês de {nomes} é do primeiro trimeste do ano')
    elif 3 < numes <= 6:
        print(f'O mês de {nomes} é do segundo trimeste do ano')
    elif 6 < numes <= 9: 
        print(f'O mês de {nomes} é do terceiro trimestre do ano')
    elif 9 < numes <= 12:
        print(f'O mês de {nomes} é do quarto trimestre do ano') 
    else:
         print('Insira número válido')

        
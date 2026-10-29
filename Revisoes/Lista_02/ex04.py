dia, mes, ano = map(int, input('Digite uma data no formato dd/mm/aaaa: ').split('/'))
if dia < 1 or dia > 31:
    print('A data informada não é valida')
if mes < 1 or mes > 12:
    print('A data informada não é valida')
if ano < 1900 or ano > 2100:
    print('A data informada não é valida')
else:
    print(f'A data informada é: {dia}/{mes}/{ano}')

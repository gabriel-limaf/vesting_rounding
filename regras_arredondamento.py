import math


def cumulative_rounding():
    lista_acoes_na_tranche = []
    acumulado = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = total_acoes / tranche_sem_cliff
        lista_acoes_na_tranche.append(acoes_na_tranche)
    # Itera sobre os itens da lista original e calcula a soma acumulada
    accumulator = 0
    for item in lista_acoes_na_tranche:
        accumulator += item
        acumulado.append(math.ceil(accumulator))
    # Calcula a diferença entre itens consecutivos da lista acumulada
    diff_list = [acumulado[i] - acumulado[i - 1] if i > 0 else acumulado[0] for i in range(len(acumulado))]
    soma_acoes_no_cliff = sum(diff_list[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + diff_list[tranches_no_cliff:]
    print(nova_lista)
    return nova_lista


def cumulative_rounding_down():
    lista_acoes_na_tranche = []
    acumulado = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = total_acoes / tranche_sem_cliff
        lista_acoes_na_tranche.append(acoes_na_tranche)
    # Itera sobre os itens da lista original e calcula a soma acumulada
    accumulator = 0
    for item in lista_acoes_na_tranche:
        accumulator += item
        acumulado.append(math.floor(accumulator))
    # Calcula a diferença entre itens consecutivos da lista acumulada
    diff_list = [acumulado[i] - acumulado[i - 1] if i > 0 else acumulado[0] for i in range(len(acumulado))]
    soma_acoes_no_cliff = sum(diff_list[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + diff_list[tranches_no_cliff:]
    print(nova_lista)
    return nova_lista


def front_loaded():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    sobra = total_acoes - sum(lista_acoes_na_tranche)
    idx = 0
    while sobra > 0:
        lista_acoes_na_tranche[idx] += 1
        sobra -= 1
        idx += 1
        if idx >= tranche_sem_cliff:
            idx = 0
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
    print(nova_lista)
    return nova_lista


def back_loaded():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    sobra = total_acoes - sum(lista_acoes_na_tranche)
    idx = len(lista_acoes_na_tranche) - 1
    print(idx)
    while sobra > 0:
        lista_acoes_na_tranche[idx] += 1
        sobra -= 1
        idx -= 1
        if idx < cliff:
            idx = len(lista_acoes_na_tranche) - 1
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
    print(nova_lista)
    return nova_lista


def front_loaded_to_single_tranche():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    lista_acoes_na_tranche[0] += acoes_restantes
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
    print(nova_lista)
    return nova_lista


def back_loaded_to_single_tranche():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    lista_acoes_na_tranche[-1] += acoes_restantes
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
    print(nova_lista)
    return nova_lista


def fractional():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = round(total_acoes / tranche_sem_cliff, 4)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    sobra = total_acoes - sum(lista_acoes_na_tranche)
    nova_lista = [soma_acoes_no_cliff + sobra] + [round(x, 4) for x in lista_acoes_na_tranche[tranches_no_cliff:]]
    nova_lista = [round(x, 4) for x in nova_lista]
    print(nova_lista)
    return nova_lista


# Dados iniciais
total_acoes = 130
vesting = 48
cliff = 12
periodicidade = 3

# Calcular Tranches
tranche_sem_cliff = math.ceil(vesting / periodicidade)
tranches_no_cliff = math.ceil(cliff / periodicidade)
total_tranches = math.ceil(tranche_sem_cliff - tranches_no_cliff + 1)

# Calcular a quantidade de ações por vesting
acoes_por_vesting = total_acoes / vesting

# Calcular a quantidade de ações no período
acoes_periodo = acoes_por_vesting * periodicidade

# Calcular a quantidade de ações restantes
acoes_restantes = total_acoes - math.floor(acoes_periodo) * tranche_sem_cliff

while True:
    arredondamento = int(input('Qual forma de arredondamento deseja selecionar?\n'
                               'Cumulative Rounding (5 - 4 - 5 - 4)	: Digite 1\n'
                               'Cumulative Round Down (4 - 5 - 4 - 5) : Digite 2\n'
                               'Front Loaded (5 - 5 - 4 - 4) : Digite 3\n'
                               'Back Loaded (4 - 4 - 5 - 5) : Digite 4\n'
                               'Front Loaded to Single Tranche (6 - 4 - 4 - 4) : Digite 5\n'
                               'Back Loaded to Single Tranche (4 - 4 - 4 - 6) : Digite 6\n'
                               'Fractional (4.5 - 4.5 - 4.5 - 4.5) : Digite 7\n'
                               'Sair : Digite 0\n'))
    if arredondamento not in [0, 1, 2, 3, 4, 5, 6, 7]:
        print('Escolha um valor válido')
        continue
    if arredondamento == 0:
        break
    if arredondamento == 1:
        cumulative_rounding()
    if arredondamento == 2:
        cumulative_rounding_down()
    if arredondamento == 3:
        front_loaded()
    if arredondamento == 4:
        back_loaded()
    if arredondamento == 5:
        front_loaded_to_single_tranche()
    if arredondamento == 6:
        back_loaded_to_single_tranche()
    if arredondamento == 7:
        fractional()

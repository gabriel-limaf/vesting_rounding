import math
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def gerar_datas_vesting(data_inicio, quantidade_tranches, intervalo_meses):
    datas = []
    for i in range(1, quantidade_tranches + 1):
        data_futura = data_inicio + relativedelta(months=i * intervalo_meses)
        datas.append(data_futura.strftime('%Y-%m-%d'))
    return datas


def cumulative_rounding():
    lista_acoes_na_tranche = []
    acumulado = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = total_acoes / tranche_sem_cliff
        lista_acoes_na_tranche.append(acoes_na_tranche)
    accumulator = 0
    for item in lista_acoes_na_tranche:
        accumulator += item
        acumulado.append(math.ceil(accumulator))
    diff_list = [acumulado[i] - acumulado[i - 1] if i > 0 else acumulado[0] for i in range(len(acumulado))]
    soma_acoes_no_cliff = sum(diff_list[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + diff_list[tranches_no_cliff:]
    return nova_lista


def cumulative_rounding_down():
    lista_acoes_na_tranche = []
    acumulado = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = total_acoes / tranche_sem_cliff
        lista_acoes_na_tranche.append(acoes_na_tranche)
    accumulator = 0
    for item in lista_acoes_na_tranche:
        accumulator += item
        acumulado.append(math.floor(accumulator))
    diff_list = [acumulado[i] - acumulado[i - 1] if i > 0 else acumulado[0] for i in range(len(acumulado))]
    soma_acoes_no_cliff = sum(diff_list[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + diff_list[tranches_no_cliff:]
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
    return nova_lista


def back_loaded():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    sobra = total_acoes - sum(lista_acoes_na_tranche)
    idx = len(lista_acoes_na_tranche) - 1
    while sobra > 0:
        lista_acoes_na_tranche[idx] += 1
        sobra -= 1
        idx -= 1
        if idx < cliff:
            idx = len(lista_acoes_na_tranche) - 1
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
    return nova_lista


def front_loaded_to_single_tranche():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    lista_acoes_na_tranche[0] += acoes_restantes
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
    return nova_lista


def back_loaded_to_single_tranche():
    lista_acoes_na_tranche = []
    for _ in range(tranche_sem_cliff):
        acoes_na_tranche = math.floor(total_acoes / tranche_sem_cliff)
        lista_acoes_na_tranche.append(acoes_na_tranche)
    soma_acoes_no_cliff = sum(lista_acoes_na_tranche[:tranches_no_cliff])
    lista_acoes_na_tranche[-1] += acoes_restantes
    nova_lista = [soma_acoes_no_cliff] + lista_acoes_na_tranche[tranches_no_cliff:]
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
    return nova_lista

# Dados iniciais
total_acoes = 130
vesting = 48
cliff = 12
periodicidade = 2
data_inicio_vesting = datetime(2023, 1, 1)

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

# Gerar datas de vesting
datas_vesting = gerar_datas_vesting(data_inicio_vesting, total_tranches, periodicidade)
print(datas_vesting)

# Selecionar a forma de arredondamento
arredondamento = int(input('Qual forma de arredondamento deseja selecionar?\n'
                           'Cumulative Rounding (5 - 4 - 5 - 4)	: Digite 1\n'
                           'Cumulative Round Down (4 - 5 - 4 - 5) : Digite 2\n'
                           'Front Loaded (5 - 5 - 4 - 4) : Digite 3\n'
                           'Back Loaded (4 - 4 - 5 - 5) : Digite 4\n'
                           'Front Loaded to Single Tranche (6 - 4 - 4 - 4) : Digite 5\n'
                           'Back Loaded to Single Tranche (4 - 4 - 4 - 6) : Digite 6\n'
                           'Fractional (4.5 - 4.5 - 4.5 - 4.5) : Digite 7\n'
                           'Sair : Digite 0\n'))
if arredondamento == 1:
    quantidade_acoes = cumulative_rounding()
elif arredondamento == 2:
    quantidade_acoes = cumulative_rounding_down()
elif arredondamento == 3:
    quantidade_acoes = front_loaded()
elif arredondamento == 4:
    quantidade_acoes = back_loaded()
elif arredondamento == 5:
    quantidade_acoes = front_loaded_to_single_tranche()
elif arredondamento == 6:
    quantidade_acoes = back_loaded_to_single_tranche()
elif arredondamento == 7:
    quantidade_acoes = fractional()
else:
    print('Escolha um valor válido')
    exit()
print(quantidade_acoes)
# Criar o dicionário combinando datas e quantidades de ações
vesting_dict = {datas_vesting[i]: quantidade_acoes[i] for i in range(len(datas_vesting))}

# Converter o dicionário para JSON
vesting_json = json.dumps(vesting_dict, indent=4)

# Imprimir o JSON resultante
print("JSON resultante:")
print(vesting_json)

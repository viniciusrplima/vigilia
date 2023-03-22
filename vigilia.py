import random
import json
import copy

def load_csv(filename):
    content = open(filename, 'r').read()
    lines = content.split('\n')
    csv = []
    for line in lines:
        csv.append(line.split('|'))
    return csv


users_req = load_csv('users.req')
users_disp = load_csv('users.disp')
disponibilidade = {}

for user_req in users_req:
    [nome, sexo, maximo_horas, maximo_dias] = user_req
    if nome not in disponibilidade.keys(): disponibilidade[nome] = {}
    disponibilidade[nome] = {
        'nome': nome, 
        'sexo': sexo, 
        'maximo_horas': int(maximo_horas),
        'maximo_dias': int(maximo_dias)
    }

for user_disp in users_disp:
    [nome, dia, inicio, fim] = user_disp
    if nome not in disponibilidade.keys(): disponibilidade[nome] = {}
    if 'horarios' not in disponibilidade[nome].keys(): disponibilidade[nome]['horarios'] = []
    disponibilidade[nome]['horarios'].append({
        'dia': dia, 
        'inicio': float(inicio), 
        'fim': float(fim)
    })

PASSO = 1
DIAS = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab']

def horarios(inicio, fim, passo):
    if inicio > fim: raise ValueError('falha no calculo dos horarios, inicio deve ser menor que fim')
    horarios = []
    while inicio < fim: 
        horarios.append(inicio)
        inicio += passo
    return horarios


def cria_registro(disp):
    registro = {}
    for pessoa in disp:
        registro[pessoa["nome"]] = {}
    return registro


def esta_disponivel(pessoa, dia, hora):
    horarios = pessoa["horarios"]
    for horario in horarios:
        if horario["dia"] == dia and hora >= horario["inicio"] and hora < horario["fim"]: 
            return True
    return False

#############################
##    REQUISITOS  LOCAIS
#############################

def maximo_horas(pessoa, registro):
    reg_pessoa = registro[pessoa["nome"]]
    return all(horas <= pessoa["maximo_horas"] for horas in reg_pessoa.values())


def maximo_dias(pessoa, registro):
    reg_pessoa = registro[pessoa["nome"]]
    return len(reg_pessoa.keys()) <= pessoa["maximo_dias"]


def respeita_requisitos(pessoa, reqs, registro):
    return all([req(pessoa, registro) for req in reqs])

##########################


def escala(inicio, fim, disp, reqs): 
    escala = {}
    registro = cria_registro(disp)
    for dia in DIAS:
        escala[dia] = {} 
        random.shuffle(disp)
        for hora in horarios(inicio, fim, PASSO):
            escala[dia][str(hora)] = []
            for pessoa in disp:
                nome = pessoa["nome"]
                registro_tmp = copy.deepcopy(registro)
                if dia not in registro_tmp[nome].keys(): registro_tmp[nome][dia] = 0
                registro_tmp[nome][dia] += PASSO
                if esta_disponivel(pessoa, dia, hora) and respeita_requisitos(pessoa, reqs, registro_tmp):
                    escala[dia][str(hora)].append(nome)
                    registro = registro_tmp
    return escala


INICIO = 13
FIM = 17

res_escala = escala(INICIO, FIM, list(disponibilidade.values()), [maximo_horas, maximo_dias])

for dia in res_escala.keys():
    print(dia)
    for hora in res_escala[dia].keys():
        participantes = ', '.join(res_escala[dia][hora])
        print(f'{hora} - {participantes}')
    print(' ')
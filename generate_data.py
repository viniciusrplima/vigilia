import random

users_req = open('users.req', 'w')
users_disp = open('users.disp', 'w')

names = ['joao', 'maria', 'jose', 'joaquim', 'sebastiao', 'carlos', 'marcos', 'vinicius', 'amanda', 'roberto', 
        'eduarda', 'luciano', 'paulo', 'alberto', 'humberto', 'jimmy', 'vitor', 'severina', 'luana', 
        'joelson', 'valdeilson', 'gabriel']

DIAS = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab']

for name in names:
    sexo = 'm'
    maximo_horas = random.randint(1,5)
    maximo_dias = random.randint(1,7)
    users_req.write(f'{name}|{sexo}|{maximo_horas}|{maximo_dias}\n')
    for i in range(random.randint(1,4)):
        dia = random.choice(DIAS)
        inicio = random.randint(8,17)
        fim = inicio + random.randint(1,4)
        if fim > 18: fim = 18
        users_disp.write(f'{name}|{dia}|{inicio}|{fim}\n')


users_req.close()
users_disp.close()
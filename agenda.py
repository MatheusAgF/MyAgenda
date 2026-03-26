import sys
import ctypes, sys
TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
DONE = 'd'
REMOVER_DO_DONE = 'R'
DESFAZER =  'D'

def printCores(texto, cor):
  print(cor + texto + RESET)


def adicionar(descricao, extras):
  data = hora = prioridade = contexto = projeto = ""
  descricao = descricao + " "

  for x in extras:
    if dataValida(x) == True: data = x + " "

    if horaValida(x) == True: hora = x + " "

    if prioridadeValida(x) == True: prioridade = x + " "
    
    if contextoValido(x) == True: contexto = x + " "
    
    if projetoValido(x) == True: projeto = x + " "

    novaAtividade = data + hora + prioridade + descricao + contexto + projeto

  if descricao != " ":
    try:
      fp = open(TODO_FILE, "a")
      fp.write(novaAtividade + "\n")
      fp.close()
    
    except IOError as err:
      print("Não foi possível escrever para o arquivo" + TODO_FILE)
      print(err)
  
  if descricao == " ":
     print("Não foi possível escrever para o arquivo" + TODO_FILE)

      
def prioridadeValida(pri):
    lista = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","ç","z","x","c","v","b","n","m"]
    prioridade = pri.lower()
    if len(pri) < 3: return False
    
    if prioridade[0] != "(" or prioridade[2] != ")": return False

    elif prioridade[1] not in lista: return False
  
    else: return True

def horaValida(horaMin):
  if len(horaMin) != 4 or not soDigitos(horaMin): return False
  
  else:
    hora = horaMin[0] + horaMin[1]
    hora = int(hora)
    minuto = horaMin[2] + horaMin[3]
    minuto = int(minuto)
  
    if hora >= 00 and hora <= 23 and minuto >= 00 and minuto <= 59:
      return True
    else: return False
    
def dataValida(data):
    if len(data) != 8: return False

    if not soDigitos(data): return False

    else:
        dia = int(data[0] + data[1])
        mes = int(data[2] + data[3])
        ano = int(data[4] + data[5] + data[6] + data[7])

        if mes == 2 and dia > 28 or dia < 1: return False
  
        elif (mes == 4 or mes == 6 or mes == 9 or mes == 11) and dia > 30 or dia < 1:
            return False 
  
        elif dia > 31 or dia < 1: return False
  
        elif mes > 12 or mes < 1: return False
  
        elif ano >= 0 and ano <= 9999: return True
                    
def projetoValido(proj):
    if len(proj) < 2: return False

    elif proj[0] != "+": return False
    
    else: return True
    
def contextoValido(cont):
    if len(cont) < 2: return False
    elif cont[0] != "@": return False
    else: return True
    
def soDigitos(numero):
  if type(numero) != str: return False

  for x in numero:
    if x < '0' or x > '9':
      return False
    
  return True


def organizar(linhas): #perfeito!
  itens = []
  for l in linhas:
    data = hora = pri = ctx = proj = desc = ''

    l = l.strip()
    tokens = l.split()

    if dataValida(tokens[0]): data = tokens.pop(0)

    if horaValida(tokens[0]): hora = tokens.pop(0)

    if prioridadeValida(tokens[0]): pri = tokens.pop(0)

    if projetoValido(tokens[-1]): proj = tokens.pop(-1)

    if contextoValido(tokens[-1]): ctx = tokens.pop(-1)

    desc = ' '.join(tokens)
    itens.append((desc, (pri, data, hora, ctx, proj)))
  return itens

def ordenarPorAno(itens):
  #[(descricao, (prioridade, data, hora, contexto, projeto))]
  if len(itens) == 0:
    return itens

  pivo = int(itens[len(itens)//2][1][1][-4:])
  menores = [x for x in itens if int(x[1][1][-4:]) < pivo]
  iguais = [x for x in itens if int(x[1][1][-4:]) == pivo]
  maiores = [x for x in itens if int(x[1][1][-4:]) > pivo]

  return ordenarPorAno(menores) + iguais + ordenarPorAno(maiores)


def ordenarPorMes(itens, cont=0):
  if cont >= len(itens): return itens

  for i in range(1, len(itens)):
    j = i - 1
    atual = itens[i]
    antecessor = itens[j]

    if int(atual[1][1][-4:]) == int(antecessor[1][1][-4:]):
      if int(antecessor[1][1][2:4]) > int(atual[1][1][2:4]):
        itens[j], itens[i] = itens[i], itens[j]

  return ordenarPorMes(itens, cont+1)

def ordenarPorDia(itens, cont=0):
  if cont >= len(itens): return itens

  for i in range(1, len(itens)):
    j = i - 1
    atual = itens[i]
    antecessor = itens[j]

    if int(atual[1][1][2:4]) == int(antecessor[1][1][2:4]):
      if int(atual[1][1][:2]) < int(antecessor[1][1][:2]):
        itens[j], itens[i] = itens[i], itens[j]

  return ordenarPorDia(itens, cont+1)

def ordenarPorHora(itens, cont=0):
  #[(descricao, (prioridade, data, hora, contexto, projeto))]
  if cont >= len(itens): return itens

  for i in range(1, len(itens)):
    j = i - 1
    atual = itens[i]
    antecessor = itens[j]

    if atual[1][1] == antecessor[1][1]:
      if atual[1][2] == '': continue

      if antecessor[1][2] == '':
        itens[j], itens[i] = itens[i], itens[j]
        continue

      if atual[1][2] < antecessor[1][2]:
        itens[j], itens[i] = itens[i], itens[j]

  return ordenarPorHora(itens, cont+1)

def ordenarPorDataHora(itens: list):
  #[(descricao, (prioridade, data, hora, contexto, projeto))]
  sem_data = [x for x in itens if x[1][1] == '']
  com_data = [x for x in itens if x[1][1] != '']

  com_data = ordenarPorAno(com_data)
  com_data = ordenarPorMes(com_data)
  com_data = ordenarPorDia(com_data)

  com_data = ordenarPorHora(com_data)
  sem_data = ordenarPorHora(sem_data)

  itens = com_data + sem_data
  return itens

def ordenarPorPrioridade(itens, cont=0):
  if cont >= len(itens): return itens

  for i in range(1, len(itens)):
    j = i - 1
    atual = itens[i][1][0]
    atual = atual.lower()
    antecessor = itens[j][1][0]
    antecessor = antecessor.lower()
    
    if atual == '': continue

    if antecessor == '':
      itens[j], itens[i] = itens[i], itens[j]
      continue

    if atual < antecessor:
      itens[j], itens[i] = itens[i], itens[j]

  return ordenarPorPrioridade(itens, cont+1)


def listar(file): #Perfeito!!
  with open(file, 'r') as arquivo:
    linhas = [linha.rstrip(' \n') for linha in arquivo]

  tarefas = organizar(linhas)
  tarefas = ordenarPorDataHora(tarefas)
  tarefas = ordenarPorPrioridade(tarefas)

  with open(file, 'w') as arquivo:
    for tarefa in tarefas:
      tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
      tarefa_list = [x for x in tarefa_list if x != '']
      tarefa_str = ' '.join(tarefa_list)
      arquivo.write(tarefa_str + '\n')

  return tarefas
  

def listarPadrao(tarefas):
  lista = []
  for i,tarefa in enumerate(tarefas):
    # tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
    tarefa_list = [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
    tarefa_list = [x for x in tarefa_list if x != '']
    tarefa_str = ' '.join(tarefa_list)

    if tarefa[1][0] == '(A)':
      printCores(f'{i+1} {tarefa_str}', BOLD + RED)

    elif tarefa[1][0] == '(B)':
      printCores(f'{i+1} {tarefa_str}', YELLOW)
    
    elif tarefa[1][0] == '(C)':
      printCores(f'{i+1} {tarefa_str}', GREEN)
    
    elif tarefa[1][0] == '(D)':
      printCores(f'{i+1} {tarefa_str}', BLUE)
    
    else:
      print(f'{i+1} {tarefa_str}')

    lista.append((tarefa[1][1], tarefa[1][2], tarefa_str, i))
  return lista

def listarPri(tarefas,pri: str):
  lista = []
  pri = pri.upper()
  entrou = False
  for i,tarefa in enumerate(tarefas):
    tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
    tarefa_list = [x for x in tarefa_list if x != '']
    tarefa_str = ' '.join(tarefa_list)

    if tarefa[1][0] == f'({pri})':
      print(f'{i+1} {tarefa_str}')
      entrou = True
      lista.append((tarefa[1][1], tarefa[1][2], tarefa_str, i))
  if not entrou:
    print('Não a tarefas com essa prioridade.')
  return lista


def listarCtx(tarefas,ctx):
  lista = []
  entrou = False
  for i,tarefa in enumerate(tarefas):
    tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
    tarefa_list = [x for x in tarefa_list if x != '']
    tarefa_str = ' '.join(tarefa_list)

    if tarefa[1][3] == ctx:
      print(f'{i+1} {tarefa_str}')
      entrou = True
      lista.append((tarefa[1][1], tarefa[1][2], tarefa_str, i))
  if not entrou:
    print('Contexto inválido ou inexistente.')
  return lista

def listarProj(tarefas,proj):
  lista = []
  entrou = False
  for i,tarefa in enumerate(tarefas):
    tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
    tarefa_list = [x for x in tarefa_list if x != '']
    tarefa_str = ' '.join(tarefa_list)

    if tarefa[1][4] == proj:
      print(f'{i+1} {tarefa_str}')
      entrou = True
      lista.append((tarefa[1][1], tarefa[1][2], tarefa_str, i))
  if not entrou:
    print('Projeto inválido ou inexistente.')
  return lista


def remover(file, num):
  lista = []
  with open(file, 'r') as todo:
    for i,tarefa in enumerate(todo):
      lista.append(tarefa)

  with open(file, 'w') as todo:
    entrou = False
    for i,tarefa in enumerate(lista):
      if num != i+1:
        todo.write(tarefa)
      if num == i+1:
        entrou = True

  print('Tarefa removida!' if entrou else 'Error: Tarefa não encontrada!')


def fazer(file, fileAdd, num):
  lista = []
  with open(file, 'r') as todo:
    for i,tarefa in enumerate(todo):
      lista.append(tarefa)

  with open(file, 'w') as todo:
    entrou = False
    for i,tarefa in enumerate(lista):
      if num != i+1:
        todo.write(tarefa)
      if num == i+1:
        entrou = True
        guardar = tarefa

  if entrou:
    print('Tarefa concluída! Salva em done!')
    with open(fileAdd, 'a') as done:
      done.write(guardar)
  else:
    print('Error: Tarefa não encontrada!')


def priorizar(num, pri):
  if pri == '#':
    pri = ''
  else:
    pri = f'({pri})'
  pri = pri.upper()
  with open(TODO_FILE, 'r') as arquivo:
    linhas = [linha.rstrip(' \n') for linha in arquivo]
  tarefas = organizar(linhas)

  entrou = False
  with open(TODO_FILE, 'w') as arquivo:
    for i,tarefa in enumerate(tarefas):

      if num == i+1:
        tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [pri] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
        tarefa_list = [x for x in tarefa_list if x != '']
        tarefa_str = ' '.join(tarefa_list)
        arquivo.write(tarefa_str + '\n')
        entrou = True

      else:
        tarefa_list = [tarefa[1][1]] + [tarefa[1][2]] + [tarefa[1][0]] + [tarefa[0]] + [tarefa[1][3]] + [tarefa[1][4]]
        tarefa_list = [x for x in tarefa_list if x != '']
        tarefa_str = ' '.join(tarefa_list)
        arquivo.write(tarefa_str + '\n')

  print('Tarefa priorizada!' if entrou else 'Error: Tarefa não encontrada!')


def processarComandos(comandos):
  if comandos[0] == ADICIONAR:
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    
  elif comandos[0] == LISTAR:
    tarefas = listar(TODO_FILE)
    try:
      comandos[1]
    except IndexError:
      return listarPadrao(tarefas)

    if 'A' <= comandos[1] <= 'z' and len(comandos[1]) == 1: 
      return listarPri(tarefas, comandos[1])

    elif contextoValido(comandos[1]): return listarCtx(tarefas,comandos[1])

    elif projetoValido(comandos[1]): return listarProj(tarefas, comandos[1])

  elif comandos[0] == REMOVER: remover(TODO_FILE, int(comandos[1]))

  elif comandos[0] == FAZER: fazer(TODO_FILE, ARCHIVE_FILE,int(comandos[1]))

  elif comandos[0] == PRIORIZAR: priorizar(int(comandos[1]),comandos[2])

  elif comandos[0] == DONE:
    tarefas = listar(ARCHIVE_FILE)
    tarefas = listarPadrao(tarefas)
    return tarefas
  
  elif comandos[0] == REMOVER_DO_DONE: remover(ARCHIVE_FILE, int(comandos[1]))

  elif comandos[0] == DESFAZER: fazer(ARCHIVE_FILE, TODO_FILE, int(comandos[1]))

  else: print("Comando inválido.")

#verifica se existe mais de um parâmetro na linha de comando
if len(sys.argv) > 1:
  processarComandos(sys.argv)
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
#processarComandos(sys.argv)
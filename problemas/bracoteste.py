import random
import numpy as np
from no import No
from problemas.problema import Problema


class BracoT(Problema):
  def __init__(self):

    # o problema ta menor pra facilitar os testes
    # mudar dps pra 10x4 com um espaco a mais pra o q o braco ta segurando


    self.num_linhas = 6

    
    self.estado_inicial = np.array([40, "0", "0", "R",
                                     "0", "0", "0", "|",
                                     20, 50, "0", "|", 
                                     30, "0", "0", "|",
                                     60, "0", "0", "|",
                                     10, "0", "0", "|",
                                     "0"])


  def iniciar(self):
    self.no_raiz = No(self.estado_inicial)
    return self.no_raiz

  # Função auxiliar para imprimir
  def imprimir(self, no):
    estado = no.estado
    maquina = ""

  # o problema ta menor pra facilitar os testes
  # mudar dps pra 10x4 com um espaco a mais pra o q o braco ta segurando 
    for i in range(self.num_linhas):
        for j in range(4):
            index = i * 4 + j
            maquina += estado[index] + " "
        maquina += "\n"

    maquina += estado[-1]
    return maquina


  def contar_caixas(self,no):
    count = 0
    index = 0
    for i in range(len(no.estado)):
      if self.verificar_numero(no, index) and no.estado[i] != "0":
        count += 1
      index +=1
    return count

#funcao precisa ter um numero % 3 = 0 de caixas pra funcionar
#verifica se tem uma pilha formada em qualquer posicao
  def testar_objetivo(self, no):
    estado = no.estado
    count_pilhas = 0
    pilhas_possiveis = np.ceil(self.contar_caixas(no) /3) 
    #print(pilhas_possiveis)
    for i in range(self.num_linhas):
      for j in range(4):
        index = i * 4 + j
        if self.verificar_numero(no, index):
          if self.verificar_numero(no, index +1) and self.verificar_numero(no, index + 2):
           # valido ou nao ter [30,30,20] ?? >= ou >
            if int(estado[index]) >= int(estado[index + 1]) and int(estado[index + 1] >= estado[index + 2]):
              count_pilhas += 1
    return count_pilhas == pilhas_possiveis

  def verificar_numero(self, no, index):
    estado = no.estado
    if estado[index] != "0" and estado[index] != "R" and estado[index] != "|":
      return True

  
  # Função que gera os sucessores válidos
  # a partir de um estado válido
  def gerar_sucessores(self, no):
    estado = no.estado
    nos_sucessores = []


    # encontra a posição do R (Braco)
    posicao = np.where(estado == "R")[0][0]

    expansoes = [self._direita, self._esquerda, self._agarrar, self._soltar, self._esquerda2, self._direita2]
    random.shuffle(expansoes)
    for expansao in expansoes:
      no_sucessor = expansao(posicao, no)
      if no_sucessor is not None: nos_sucessores.append(no_sucessor)

    return nos_sucessores

  # limitantes
  # o formato ta assim, o braco so se move na quarta coluna
  # as pilhas de caixas sao as linhas da esquerda pra direita
  # o ultimo espaco e o q o braco ta segurando
  # | 00 | 01 | 02 | 03 |
  # | 04 | 05 | 06 | 07 |
  # | 08 | 09 | 10 | 11 |
  # | 12 | 13 | 14 | 15 |
  # | 16 | 17 | 18 | 19 |
  # | 20 | 21 | 22 | 23 |
  # | 24 | 25 | 26 | 27 |
  # | 28 | 29 | 30 | 31 |
  # | 32 | 33 | 34 | 35 |
  # | 36 | 37 | 38 | 39 |
  # | 40 |



  def _esquerda(self, posicao, no):
    # movimento para esquerda fazendo swap apenas na ultima coluna
    if posicao not in [0, 1, 2, 3] and no.estado[posicao - 4] == "|":
      
      sucessor = np.copy(no.estado)
      sucessor[posicao] = sucessor[posicao - 4]
      sucessor[posicao - 4] = "R"
      return No(sucessor, no, "⬅️")
    else:
      None

  def _esquerda2(self, posicao, no):
    # movimento para esquerda fazendo swap apenas na ultima coluna
    if posicao not in [3, 7, 11] and no.estado[posicao - 8] == "|":

      sucessor = np.copy(no.estado)
      sucessor[posicao] = sucessor[posicao - 8]
      sucessor[posicao - 8] = "R"
      return No(sucessor, no, "⬅️⬅️")
    else:
      None

  def _direita(self, posicao, no):
    # movimento para direita fazendo swap apenas na ultima coluna
    if posicao not in [21, 22, 23, 24] and no.estado[posicao + 4] == "|":
      
      sucessor = np.copy(no.estado)
      sucessor[posicao] = sucessor[posicao + 4]
      sucessor[posicao + 4] = "R"
      return No(sucessor, no, "➡️")
    else:
      None

  def _direita2(self, posicao, no):
    # movimento para direita fazendo swap apenas na ultima coluna
    if posicao not in [23,19,15] and no.estado[posicao + 8] == "|":

      sucessor = np.copy(no.estado)
      sucessor[posicao] = sucessor[posicao + 8]
      sucessor[posicao + 8] = "R"
      return No(sucessor, no, "➡️➡️")
    else:
      None

  # funcao de agarrar feia q funciona
  # ta tudo feio e com certeza tem um jeito melhor de fazer isso
  # o "." representa um espaco vazio
  def _agarrar(self, posicao, no):
   
    if no.estado[-1] == "0":
      if no.estado[posicao - 3] != "0" and no.estado[posicao -2] == "0" and no.estado[posicao -1] == "0":
        sucessor = np.copy(no.estado)
        sucessor[-1] = no.estado[posicao - 3]
        sucessor[posicao - 3] = "0"
        return No(sucessor, no, "Segurou BASE")
      elif no.estado[posicao - 3] != "0":
        sucessor = np.copy(no.estado)
        sucessor[-1] = no.estado[posicao - 2]
        sucessor[posicao - 2] = "0"
        return No(sucessor, no, "Segurou MEIO")
      
    None

  
  def _soltar(self, posicao, no):
    # verifica se tem algo nos dois primeiros espaços da pilha, se tiver coloca em cima
    # ["30","20","aqui"]
    if no.estado[-1] != "0":
      if no.estado[posicao - 3] != "0" and no.estado[posicao -2] != "0" and no.estado[posicao -1] == "0":
        sucessor = np.copy(no.estado)
        sucessor[posicao - 1] = no.estado[-1]
        sucessor[-1] = "0"
        return No(sucessor, no, "Soltou TOPO")
      # verifica se tem algo no primeiro espaco da pilha, se tiver coloca no espaco do 
      # meio (em cima do primeiro) 
      # ["30","aqui","0"]
      elif no.estado[posicao - 3] != "0" and no.estado[posicao -2] == "0":
        sucessor = np.copy(no.estado)
        sucessor[posicao - 2] = no.estado[-1]
        sucessor[-1] = "0"
        return No(sucessor, no, "Soltou MEIO")
      # verifica se a pilha esta vazia, se tiver coloca no primeiro espaco da pilha.
      # ["aqui","0","0"]
      elif no.estado[posicao - 3] == "0":
        sucessor = np.copy(no.estado)
        sucessor[posicao -3] = no.estado[-1]
        sucessor[-1] = "0"
        return No(sucessor, no, "Soltou BASE")
    else:
     None

  def custo(self, no, no_sucessor):
    valor_custo = 1
    estadoAtual = np.where(no.estado == "R")[0][0]
    estadoFuturo = np.where(no_sucessor.estado == "R")[0][0]

    # ato de pegar uma caixa n tem custo
    if estadoFuturo - estadoAtual == 0:
      return 0


    if abs((estadoFuturo - estadoAtual) / 4) > 0:
      valor_custo += abs((estadoFuturo - estadoAtual) * 0.75)

    # verifica se ta segurando uma caixa, se nao, custo 1
    # se sim calcula o custo baseado no peso da caixa
    if no.estado[-1] == "0":
      return valor_custo
    else:
      valor_custo += int(no.estado[-1]) / 10
      return valor_custo

    
  def heuristica(self, no):
    estado = no.estado
    lista = []
    indice = 0
    for i in range(len(estado) -1):
      if self.verificar_numero(no, i):
        lista.append(int(estado[i]))
    
    soma = 0
  
    lista1 = np.sort(lista)[::-1]
    
    for i in range(len(lista)):
      soma = soma + abs(lista1[i] - lista[i])

    return soma


    
      

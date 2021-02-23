from collections import defaultdict

class Heap():

    def __init__(self):
        self.vetor = []
        self.tamanho = 0
        self.pos = []

    def minHeapify(self, i):
        menor = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2

        if esquerda < self.tamanho and self.vetor[esquerda][1] < self.vetor[menor][1]:
            menor = esquerda

        if direita < self.tamanho and self.vetor[direita][1] < self.vetor[menor][1]:
            menor = direita

        if menor != i:
            self.pos[self.vetor[menor][0]] = i
            self.pos[self.vetor[i][0]] = menor

            self.trocaMinHeap(menor, i)
            self.minHeapify(menor)

    def trocaMinHeap(self, a, b):
        self.vetor[a], self.vetor[b] = self.vetor[b], self.vetor[a]

    def tiraMin(self):
        if self.tamanho == 0:
            return

        raiz = self.vetor[0]

        ultimoNode = self.vetor[self.tamanho - 1]
        self.vetor[0] = ultimoNode

        self.pos[ultimoNode[0]] = 0
        self.pos[raiz[0]] = self.tamanho - 1

        self.tamanho = self.tamanho - 1
        self.minHeapify(0)

        return raiz

    def diminui(self, v, dist):
        i = v
        self.vetor[v][1] = dist

        while i > 0 and self.vetor[i][1] < self.vetor[(i - 1)//2][1]:
            self.pos[self.vetor[i][0]] = (i-1)//2
            self.pos[self.vetor[(i-1)//2][0]] = i
            self.trocaMinHeap(i, (i-1)//2)

            i = (i-1)//2

    def isInHeap(self, v):
        if self.pos[v] < self.tamanho:
            return True
        return False

class Grafo():

    def __init__(self, v):
        self.v = v
        self.grafo = defaultdict(list)

    def addAresta(self, u, v, w):
        novoVertice = [v, w]
        self.grafo[u].insert(0, novoVertice)

    def dijkstra(self, u):
        v = self.v
        dist = []                          #lista de distancias

        minHeap = Heap()

        for i in range(v):
            dist.append(999999999)
            minHeap.vetor.append([i, dist[i]])
            minHeap.pos.append(i)

        minHeap.tamanho = v

        dist[u] = 0
        minHeap.diminui(u, dist[u])

        while minHeap.tamanho != 0:
            novoNode = minHeap.tiraMin()
            u = novoNode[0]

            for j in self.grafo[u]:
                k = j[0]
                if minHeap.isInHeap(k) and dist[u] != 999999999 and j[1] + dist[u] < dist[k]:
                    dist[k] = j[1] + dist[u]

                    minHeap.diminui(k, dist[k])

        return dist

node = int(input('Qual a quantidade de vértices do grafo?'))
arestas = int(input('Qual a quantidade de arestas do grafo?'))

graph = Grafo(node)

for i in range(arestas):
    aux = input().split(' ')
    graph.addAresta(int(aux[0]) - 1, int(aux[1]) - 1, int(aux[2]))

nodeOrigem = int(input('Qual o neuronio de origem? ')) - 1
nodeDestino = int(input('Qual o neuronio de destino? ')) - 1

dist = graph.dijkstra(nodeOrigem)
resp = dist[nodeDestino]

if resp != 999999999:
    print('O numero de sinapses minima é: ' + str(resp))
else:
    print('Não existe sinapses entre os neuronios')

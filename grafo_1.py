def criar_grafo():
    """
    Retorna um novo grafo vazio.
    Passos:
    1. Criar um dicionário vazio: {}
    2. Retornar o dicionário (representa o grafo)
    """
    grafo = dict()
    return grafo


def inserir_vertice(grafo: dict, vertice: str):
    """
    Insere um vértice no grafo, sem arestas iniciais.
    Passos:
    1. Verificar se 'vertice' já é chave em grafo.
    2. Se não for, criar entrada grafo[vertice] = []
    3. Se já existir, não fazer nada (ou avisar)
    """
    if vertice not in grafo:
        grafo[vertice] = []
    else:
        print(f"O vértice {vertice} já existe no grafo.")

    return grafo


def inserir_aresta(grafo: dict, origem: str, destino: str, nao_direcionado=False):
    """
    Adiciona aresta entre origem e destino.
    Passos:
    1. Garantir que 'origem' e 'destino' existam no grafo (inserir se necessário).
    2. adicionar destino como vizinho de origem (append).
    3. Se for Nâo Direcionado, também:
         - adicionar origem como vizinho de destino
    """

    if origem not in grafo:
        inserir_vertice(grafo, origem)
    if destino not in grafo:
        inserir_vertice(grafo, destino)
        
    grafo[origem].append(destino)
    if nao_direcionado:
        grafo[destino].append(origem)

    return grafo

def vizinhos(grafo: dict, vertice: str):
    """
    Retorna a lista de vizinhos de 'vertice'.
    Passos:
    1. Se 'vertice' estiver em grafo, retornar grafo[vertice] (lista).
    2. Se não existir, retornar lista vazia ou sinalizar erro.
    """

    if vertice in grafo:
        return grafo[vertice]
    else:
        return []

def listar_vizinhos(grafo: dict, vertice: str):
    """
    Função semântica: imprimir/retornar os vizinhos de 'vertice'.
    Passos:
    1. Obter lista = vizinhos(grafo, vertice)
    2. Retornar/imprimir essa lista (ou informar que o vértice não existe)
    """
    
    lista = vizinhos(grafo, vertice)
    if lista:
        return lista
    else:
        return f"O vértice {vertice} não existe no grafo ou não possui vizinhos."
    

def exibir_grafo(grafo: dict):
    """
    Exibe o grafo em forma legível (lista de adjacência).
    Passos:
    1. Para cada vertice em ordem
         - imprimir: vertice -> vizinhos
    """
    for vertice in grafo:
        print(f"{vertice} -> {grafo[vertice]}")


def remover_aresta(grafo: dict, origem: str, destino: str, nao_direcionado=False):
    """
    Remove a aresta entre origem e destino.
    Passos:
    1. Verificar se 'origem' existe; se não, terminar.
    2. Se destino estiver em grafo[origem], remover essa ocorrência.
    3. Se for não direcionado, também:
         - verificar se 'destino' existe e remover 'origem' de grafo[destino] se presente.
    """
    
    if origem not in grafo:
        return grafo

    else:
        if destino in grafo[origem]:
            grafo[origem].remove(destino)
    if nao_direcionado:
        if destino in grafo:
            if origem in grafo[destino]:
                grafo[destino].remove(origem)

    return grafo



def remover_vertice(grafo, vertice, nao_direcionado=True):
    """
    Remove um vértice e todas as arestas que o tocam.
    Passos:
    1. Verificar se 'vertice' existe em grafo; se não, terminar.
    2. Para cada outro vertice no grafo:
         - se 'vertice' estiver na lista de vizinhos, remover essa aresta.
    3. Remover o vertice do grafo
    4. Opcional: retornar confirmação/erro.
    """
    if vertice in grafo:
        for v in list(grafo.keys()):
            if vertice in grafo[v]:
                grafo[v].remove(vertice)
        del grafo[vertice]
    else:
        print(f"O vértice {vertice} não existe no grafo.")

    return grafo



def existe_aresta(grafo, origem, destino):
    """
    Verifica se existe aresta direta origem -> destino.
    Passos:
    1. Verificar se 'origem' é chave no grafo.
    2. Retornar True se 'destino' estiver em grafo[origem], caso contrário False.
    """
    if origem in grafo:
        return destino in grafo[origem]
    return False


def grau_vertices(grafo):
    """
    Calcula e retorna o grau (out, in, total) de cada vértice.
    Passos:
    1. Inicializar um dict de graus vazia
    2. Para cada vertice, colocar no dict uma estrutura com in, out e total zerado
    3. Para cada u em grafo:
         - out_degree[u] = tamanho de vizinhos
         - para cada v em grafo:
            - verificar se u está na lista de vizinho de v,
            - caso esteja, adicionar +1 para o grau de entrada de u
    4. Calcular o grau total somando entrada + saida
    5. Retornar uma estrutura contendo out,in,total por vértice (ex: dict de tuplas).
    """
    graus = {}
    for vertice in grafo:
        graus[vertice] = {'in': 0, 'out': len(grafo[vertice]), 'total': 0}

    for u in grafo:
        for v in grafo:
            if u in grafo[v]:
                graus[u]['in'] += 1

    for vertice in graus:
        graus[vertice]['total'] = graus[vertice]['in'] + graus[vertice]['out']

    return graus


def percurso_valido(grafo, caminho):
    """
    Verifica se uma sequência específica de vértices (caminho) é válida:
    i.e., se existem arestas consecutivas entre os nós do caminho.
    Passos:
    1. Se caminho tiver tamanho < 2, retornar True (trivial).
    2. Para i de 0 até len(caminho)-2:
         - origem = caminho[i], destino = caminho[i+1]
         - se não existe_aresta(grafo, origem, destino): retornar False
    3. Se todas as arestas existirem, retornar True.
    """
    if len(caminho) < 2:
        return True

    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]
        if not existe_aresta(grafo, origem, destino):
            return False

    return True




def main():
    """
    Crie um menu onde seja possível escolher qual ação deseja realizar
    ex:
        1 - Mostrar o Grafo
        2 - inserir vertice
        3 - inserir aresta
        4 - remover vértice.
        ....
    """
    grafo = criar_grafo()
    while True:
        print(" Menu de operações do Grafo ")
        print("1 - Mostrar o Grafo")
        print("2 - Inserir vértice")
        print("3 - Inserir aresta")
        print("4 - Remover vértice")
        print("5 - Remover aresta")
        print("6 - Listar vizinhos de um vértice")
        print("7 - Verificar existência de aresta")
        print("8 - Calcular grau dos vértices")
        print("9 - Verificar percurso válido")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            exibir_grafo(grafo)
        elif opcao == '2':
            vertice = input("Digite o vértice a ser inserido: ")
            grafo = inserir_vertice(grafo, vertice)
        elif opcao == '3':
            origem = input("Digite o vértice de origem: ")
            destino = input("Digite o vértice de destino: ")
            grafo = inserir_aresta(grafo, origem, destino)
        elif opcao == '4':
            vertice = input("Digite o vértice a ser removido: ")
            grafo = remover_vertice(grafo, vertice)
        elif opcao == '5':
            origem = input("Digite o vértice de origem: ")
            destino = input("Digite o vértice de destino: ")
            grafo = remover_aresta(grafo, origem, destino)
        elif opcao == '6':
            vertice = input("Digite o vértice para listar seus vizinhos: ")
            print(listar_vizinhos(grafo, vertice))
        elif opcao == '7':
            origem = input("Digite o vértice de origem: ")
            destino = input("Digite o vértice de destino: ")
            if existe_aresta(grafo, origem, destino):
                print(f"A aresta de {origem} para {destino} existe.")
            else:
                print(f"A aresta de {origem} para {destino} não existe.")
        elif opcao == '8':
            graus = grau_vertices(grafo)
            for vertice, grau in graus.items():
                print(f"Vértice: {vertice}, Grau de entrada: {grau['in']}, Grau de saída: {grau['out']}, Grau total: {grau['total']}")
        elif opcao == '9':
            caminho = input("Digite o caminho (vértices separados por vírgula): ").split(',')
            if percurso_valido(grafo, caminho):
                print("O percurso é válido.")
            else:
                print("O percurso não é válido.")
        elif opcao == '0':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

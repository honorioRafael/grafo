import sys

def criar_grafo():
    """
    Cria e retorna uma estrutura de grafo com lista de arestas e lista de vértices.

    Passos:
    1. Criar uma lista vazia chamada 'vertices'.
    2. Criar uma lista vazia chamada 'arestas', onde cada elemento será uma lista de tamanho 2 (origem, destino)
    3. Retornar vertices e arestas
    """
    vertices = []
    arestas = []
    return vertices, arestas


def inserir_vertice(vertices, vertice):
    """
    Adiciona um novo vértice no grafo.

    Passos:
    1. Verificar se o vértice já existe em 'vertices'.
    2. Se não existir, adicionar à lista 'vertices'.
    """
    if vertice not in vertices:
        vertices.append(vertice)
        return True
    return False

def inserir_aresta(vertices, arestas, origem, destino, nao_direcionado=False):
    """
    Adiciona uma aresta entre dois vértices.

    Passos:
    1. Garantir que 'origem' e 'destino' existam em 'vertices'.
       - Se não existirem, chamar 'inserir_vertice' para adicioná-los.
    2. Adicionar uma lista [origem, destino] na lista 'arestas'.
    3. Se nao_direcionado=True, adicionar também [destino, origem].
    """
    inserir_vertice(vertices, origem)
    inserir_vertice(vertices, destino)

    aresta = [origem, destino]
    if aresta not in arestas:
        arestas.append(aresta)

    if nao_direcionado:
        aresta_inversa = [destino, origem]
        if aresta_inversa not in arestas:
            arestas.append(aresta_inversa)

def remover_aresta(arestas, origem, destino, nao_direcionado=False):
    """
    Remove uma aresta entre dois vértices.

    Passos:
    1. Percorrer a lista de Arestas procurando [origem, destino]
    2. Se encontrar, remover
    3. Se nao_direcionado=True, também procurar por [destino, origem]
    """
    aresta = [origem, destino]
    if aresta in arestas:
        arestas.remove(aresta)

    if nao_direcionado:
        aresta_inversa = [destino, origem]
        if aresta_inversa in arestas:
            arestas.remove(aresta_inversa)

def remover_vertice(vertices, arestas, vertice):
    """
    Remove um vértice e todas as arestas conectadas a ele.

    Passos:
    1. Verificar se o vértice existe na lista de vertices.
    2. Caso encontrado, remover o vértice da lista 'vertices'.
    3. Percorrer a lista de 'arestas' e remover todas onde o vértice aparece
       como origem ou destino.
    """
    if vertice in vertices:
        vertices.remove(vertice)
    else:
        return

    arestas_a_manter = []
    for aresta in arestas:
        origem, destino = aresta
        if origem != vertice and destino != vertice:
            arestas_a_manter.append(aresta)

    arestas.clear()
    arestas.extend(arestas_a_manter)

def existe_aresta(arestas, origem, destino):
    """
    Verifica se existe uma aresta entre origem e destino.

    Passos:
    1. Percorrer a lista de aresta procurando [origem, destino]
    2. Retornar True se encontrar
    3. Caso não encontre na lista, retornar False no final.
    """
    return [origem, destino] in arestas


def vizinhos(vertices, arestas, vertice):
    """
    Retorna a lista de vizinhos (vértices alcançáveis a partir de 'vertice').

    Passos:
    1. Criar uma lista vazia chamada 'vizinhos'.
    2. Percorrer todas as arestas [origem, destino].
    3. Se origem == vertice, adicionar destino na lista de vizinhos.
    4. Retornar a lista final.
    """
    lista_vizinhos = []
    for origem, destino in arestas:
        if origem == vertice:
            if destino not in lista_vizinhos:
                lista_vizinhos.append(destino)
    return lista_vizinhos


def grau_vertices(vertices, arestas):
    """
    Calcula o grau de entrada, saída e total de cada vértice.

    Passos:
    1. Criar um dicionário vazio 'graus'.
    2. Inicializar o dicionário para todos os vértices.
    3. Percorrer todas as arestas [origem, destino] e contar:
       - Grau de saída para a 'origem'.
       - Grau de entrada para o 'destino'.
       - Calcular o grau total (entrada + saída).
    4. Retornar o dicionário 'graus' para cada vértice.
    """
    graus = {}

    for v in vertices:
        graus[v] = {'entrada': 0, 'saida': 0, 'total': 0}

    for origem, destino in arestas:
        if origem in graus:
            graus[origem]['saida'] += 1
            graus[origem]['total'] += 1
        
        if destino in graus:
            graus[destino]['entrada'] += 1
            graus[destino]['total'] += 1
            
    return graus


def percurso_valido(arestas, caminho):
    """
    Verifica se um percurso é possível (seguindo as arestas na ordem dada).

    Passos:
    1. Percorrer o caminho de 0 até len(caminho) - 2.
    2. Para cada par consecutivo (u, v):
          - Verificar se (u, v) existe na lista de 'arestas' (funcao existe_aresta).
          - Se alguma não existir, retornar False.
    3. Se todas existirem, retornar True.
    """
    if len(caminho) < 2:
        return True

    for i in range(len(caminho) - 1):
        u = caminho[i]
        v = caminho[i+1]
        
        if not existe_aresta(arestas, u, v):
            return False
            
    return True


def listar_vizinhos(vertices, arestas, vertice):
    """
    Exibe os vizinhos de um vértice.

    Passos:
    1. Chamar a função vizinhos() para obter a lista.
    2. Exibir a lista formatada.
    """
    if vertice not in vertices:
        print(f"Vértice '{vertice}' não existe no grafo.")
        return

    lista_de_vizinhos = vizinhos(vertices, arestas, vertice)

    if not lista_de_vizinhos:
        print(f"Vértice '{vertice}' não possui vizinhos (de saída).")
    else:
        vizinhos_str = ', '.join(map(str, lista_de_vizinhos))
        print(f"Vizinhos de '{vertice}': {vizinhos_str}")


def exibir_grafo(vertices, arestas):
    """
    Exibe todas as arestas do grafo.

    Passos:
    1. Exibir a lista de vértices.
    2. Exibir todas as arestas no formato (origem -> destino).
    """
    print("\n--- Exibindo Grafo ---")
    print(f"Vértices: {vertices}")
    print("Arestas:")
    if not arestas:
        print("  (Nenhuma aresta)")
    else:
        for origem, destino in arestas:
            print(f"  {origem} -> {destino}")
    print("------------------------")


def main():
    print("Criando novo grafo...")
    vertices, arestas = criar_grafo()

    print("Inserindo arestas não-direcionadas (A-B, B-C, C-A)...")
    inserir_aresta(vertices, arestas, 'A', 'B', nao_direcionado=True)
    inserir_aresta(vertices, arestas, 'B', 'C', nao_direcionado=True)
    inserir_aresta(vertices, arestas, 'C', 'A', nao_direcionado=True)
    
    print("Inserindo aresta direcionada (C->D)...")
    inserir_aresta(vertices, arestas, 'C', 'D', nao_direcionado=False)
    
    exibir_grafo(vertices, arestas)

    print("\nCalculando graus dos vértices...")
    graus = grau_vertices(vertices, arestas)
    for vertice, g in graus.items():
        print(f"  {vertice}: Entrada={g['entrada']}, Saída={g['saida']}, Total={g['total']}")

    print("\nListando vizinhos de 'C'...")
    listar_vizinhos(vertices, arestas, 'C') 

    print("Listando vizinhos de 'D'...")
    listar_vizinhos(vertices, arestas, 'D') 

    print("\nVerificando existência de arestas...")
    print(f"Existe 'A' -> 'B'? {existe_aresta(arestas, 'A', 'B')}") 
    print(f"Existe 'B' -> 'A'? {existe_aresta(arestas, 'B', 'A')}") 
    print(f"Existe 'C' -> 'D'? {existe_aresta(arestas, 'C', 'D')}") 
    print(f"Existe 'D' -> 'C'? {existe_aresta(arestas, 'D', 'C')}") 

    print("\nVerificando percursos...")
    caminho_valido = ['A', 'B', 'C', 'D']
    caminho_invalido = ['A', 'D']
    print(f"Percurso {caminho_valido} é válido? {percurso_valido(arestas, caminho_valido)}")
    print(f"Percurso {caminho_invalido} é válido? {percurso_valido(arestas, caminho_invalido)}")

    print("\nRemovendo aresta não-direcionada (A-B)...")
    remover_aresta(arestas, 'A', 'B', nao_direcionado=True)
    exibir_grafo(vertices, arestas)

    print("\nRemovendo vértice 'C' (e todas as suas arestas)...")
    remover_vertice(vertices, arestas, 'C')
    exibir_grafo(vertices, arestas)


if __name__ == "__main__":
    main()
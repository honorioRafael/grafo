from typing import List, Tuple, Dict, Any
import json

def criar_grafo() -> Tuple[List[List[int]], List[str]]:
    """
    Cria e retorna uma matriz de adjacência vazia e uma lista de vértices.

    Passos:
    1. Criar uma lista vazia chamada matriz (para armazenar as conexões).
    2. Criar uma lista vazia chamada vertices (para armazenar os nomes dos vértices).
    3. Retornar (matriz, vertices).
    """
    matriz: List[List[int]] = []
    vertices: List[str] = []
    return (matriz, vertices)


def inserir_vertice(matriz: List[List[int]], vertices: List[str], vertice: str) -> Tuple[List[List[int]], List[str]]:
    """
    Adiciona um novo vértice ao grafo.

    Passos:
    1. Verificar se o vértice já existe em 'vertices'.
    2. Caso não exista:
        - Adicionar o vértice à lista 'vertices'.
        - Aumentar o tamanho da matriz:
            a) Para cada linha existente, adicionar um valor 0 no final (nova coluna).
            b) Adicionar uma nova linha com zeros do tamanho atualizado.
    """
    if vertice not in vertices:
        vertices.append(vertice)
        
        for linha in matriz:
            linha.append(0)
        
        nova_linha = [0] * len(vertices)
        matriz.append(nova_linha)

    return (matriz, vertices)


def inserir_aresta(matriz: List[List[int]], vertices: List[str], origem: str, destino: str, nao_direcionado=False) -> Tuple[List[List[int]], List[str]]:
    """
    Adiciona uma aresta entre dois vértices.

    Passos:
    1. Garantir que 'origem' e 'destino' existam em 'vertices':
        - Se não existirem, chamar 'inserir_vertice' para adicioná-los.
    2. Localizar o índice da origem (i) e do destino (j).
    3. Marcar a conexão na matriz: matriz[i][j] = 1.
    4. Se nao_direcionado=True, também marcar a conexão inversa matriz[j][i] = 1.
    """
    if origem not in vertices:
        inserir_vertice(matriz, vertices, origem)

    if destino not in vertices:
        inserir_vertice(matriz, vertices, destino)
    
    try:
        i = vertices.index(origem)
        j = vertices.index(destino)
    except ValueError as e:
        print(f"Erro ao localizar vértices: {e}")
        return (matriz, vertices)

    matriz[i][j] = 1
    
    if nao_direcionado:
        matriz[j][i] = 1

    return (matriz, vertices)


def remover_vertice(matriz: List[List[int]], vertices: List[str], vertice: str) -> Tuple[List[List[int]], List[str]]:
    """
    Remove um vértice e todas as arestas associadas.

    Passos:
    1. Verificar se o vértice existe em 'vertices'.
    2. Caso exista:
        - Descobrir o índice correspondente (usando vertices.index(vertice)).
        - Remover a linha da matriz na posição desse índice.
        - Remover a coluna (mesmo índice) de todas as outras linhas.
        - Remover o vértice da lista 'vertices'.
    """
    if vertice in vertices:
        idx = vertices.index(vertice)
        
        matriz.pop(idx)
        
        for linha in matriz:
            linha.pop(idx)
            
        vertices.pop(idx)
        
    return (matriz, vertices)


def remover_aresta(matriz: List[List[int]], vertices: List[str], origem: str, destino: str, nao_direcionado=False) -> Tuple[List[List[int]], List[str]]:
    """
    Remove uma aresta entre dois vértices.

    Passos:
    1. Verificar se ambos os vértices existem.
    2. Localizar os índices (i e j).
    3. Remover a aresta: matriz[i][j] = 0.
    4. Se nao_direcionado=True, também remover a inversa: matriz[j][i] = 0.
    """
    if origem in vertices and destino in vertices:
        i = vertices.index(origem)
        j = vertices.index(destino)
        
        matriz[i][j] = 0
        
        if nao_direcionado:
            matriz[j][i] = 0
            
    return (matriz, vertices)


def existe_aresta(matriz: List[List[int]], vertices: List[str], origem: str, destino: str) -> bool:
    """
    Verifica se existe uma aresta direta entre dois vértices.

    Passos:
    1. Verificar se ambos os vértices existem em 'vertices'.
    2. Obter os índices (i, j).
    3. Retornar True se matriz[i][j] == 1, caso contrário False.
    """
    if origem in vertices and destino in vertices:
        i = vertices.index(origem)
        j = vertices.index(destino)
        
        return matriz[i][j] == 1
        
    return False


def vizinhos(matriz: List[List[int]], vertices: List[str], vertice: str) -> List[str]:
    """
    Retorna a lista de vizinhos (vértices alcançáveis a partir de 'vertice').

    Passos:
    1. Verificar se 'vertice' existe em 'vertices'.
    2. Obter o índice 'i' correspondente.
    3. Criar uma lista de vizinhos vazia
    4. Para cada item da linha matriz[i], verificar se == 1
        - Adicionar o vértice correspondente na lista de vizinhos
    5. Retornar essa lista.
    """
    lista_vizinhos = []
    
    if vertice in vertices:
        i = vertices.index(vertice)
        
        linha_do_vertice = matriz[i]
        for j in range(len(linha_do_vertice)):
            if linha_do_vertice[j] == 1:
                lista_vizinhos.append(vertices[j])
                
    return lista_vizinhos


def _is_symmetric(matriz: List[List[int]]) -> bool:
    """Função auxiliar para verificar se a matriz é simétrica (grafo não-direcionado)."""
    n = len(matriz)
    if n == 0:
        return True
    
    for i in range(n):
        if len(matriz[i]) != n:
            return False
        
        for j in range(i + 1, n):
            if matriz[i][j] != matriz[j][i]:
                return False
    return True


def grau_vertices(matriz: List[List[int]], vertices: List[str]) -> Dict[str, Any]:
    """
    Calcula o grau de entrada, saída e total de cada vértice.
    Detecta automaticamente se o grafo é direcionado ou não pela simetria da matriz.

    Passos:
    1. Verificar se a matriz é simétrica (não-direcionado) ou não (direcionado).
    2. Criar um dicionário vazio 'graus'.
    3. Para cada vértice i:
        - Se não-direcionado:
            - Grau = somar valores da linha i.
            - graus[vértice] = grau
        - Se direcionado:
            - Grau de saída: somar os valores da linha i.
            - Grau de entrada: somar os valores da coluna i.
            - Grau total = entrada + saída.
            - graus[vértice] = {"saida": x, "entrada": y, "total": z}
    4. Retornar 'graus'.
    """
    nao_direcionado = _is_symmetric(matriz)
    
    graus: Dict[str, Any] = {}
    num_vertices = len(vertices)

    for i in range(num_vertices):
        v = vertices[i]
        
        if nao_direcionado:
            grau = sum(matriz[i])
            graus[v] = grau
        else:
            grau_saida = sum(matriz[i])
            grau_entrada = sum(matriz[k][i] for k in range(num_vertices))
            
            graus[v] = {
                "saida": grau_saida,
                "entrada": grau_entrada,
                "total": grau_saida + grau_entrada
            }
            
    return graus


def percurso_valido(matriz: List[List[int]], vertices: List[str], caminho: List[str]) -> bool:
    """
    Verifica se um percurso (sequência de vértices) é possível no grafo.

    Passos:
    1. Percorrer a lista 'caminho' de forma sequencial (de 0 até len-2).
    2. Para cada par consecutivo (u, v):
        - Verificar se existe_aresta(matriz, vertices, u, v) é True.
        - Se alguma não existir, retornar False.
    3. Se todas existirem, retornar True.
    """
    if not caminho or len(caminho) < 2:
        return True
        
    for i in range(len(caminho) - 1):
        u = caminho[i]
        v = caminho[i+1]
        
        if not existe_aresta(matriz, vertices, u, v):
            return False
            
    return True


def listar_vizinhos(matriz: List[List[int]], vertices: List[str], vertice: str):
    """
    Exibe (ou retorna) os vizinhos de um vértice.

    Passos:
    1. Verificar se o vértice existe.
    2. Chamar a função vizinhos() para obter a lista.
    3. Exibir a lista formatada (ex: print(f"Vizinhos de {v}: {lista}")).
    """
    if vertice not in vertices:
        print(f"Erro: Vértice '{vertice}' não encontrado no grafo.")
        return
        
    lista_de_vizinhos = vizinhos(matriz, vertices, vertice)
    
    if not lista_de_vizinhos:
        print(f"O vértice '{vertice}' não possui vizinhos de saída.")
    else:
        vizinhos_str = ", ".join(lista_de_vizinhos)
        print(f"Vizinhos de '{vertice}': {vizinhos_str}")


def exibir_grafo(matriz: List[List[int]], vertices: List[str]):
    """
    Exibe o grafo em formato de matriz de adjacência.

    Passos:
    1. Exibir cabeçalho com o nome dos vértices.
    2. Para cada linha i:
        - Mostrar o nome do vértice.
        - Mostrar os valores da linha (0 ou 1) separados por espaço.
    """
    if not vertices:
        print("Grafo vazio.")
        return

    print("      ", end="") 
    for v in vertices:
        print(f"{v:^4}", end="")
    
    print("\n" + "------" * (len(vertices) + 1))

    for i in range(len(vertices)):
        print(f"{vertices[i]:<5} |", end="")
        
        for val in matriz[i]:
            print(f"{val:^4}", end="")
        
        print()


def main():
    """
    Função principal para testar as operações do grafo.
    """
    NAO_DIRECIONADO = True
    
    g_matriz, g_vertices = criar_grafo()
    print("--- Criando Grafo ---")

    g_matriz, g_vertices = inserir_vertice(g_matriz, g_vertices, "A")
    g_matriz, g_vertices = inserir_vertice(g_matriz, g_vertices, "B")
    g_matriz, g_vertices = inserir_vertice(g_matriz, g_vertices, "C")
    g_matriz, g_vertices = inserir_vertice(g_matriz, g_vertices, "D")
    
    print("Grafo após inserir A, B, C, D:")
    exibir_grafo(g_matriz, g_vertices)

    print("\n--- Inserindo Arestas (Não-Direcionado) ---")
    g_matriz, g_vertices = inserir_aresta(g_matriz, g_vertices, "A", "B", NAO_DIRECIONADO)
    g_matriz, g_vertices = inserir_aresta(g_matriz, g_vertices, "B", "C", NAO_DIRECIONADO)
    g_matriz, g_vertices = inserir_aresta(g_matriz, g_vertices, "A", "C", NAO_DIRECIONADO)
    g_matriz, g_vertices = inserir_aresta(g_matriz, g_vertices, "C", "D", NAO_DIRECIONADO)

    print("Grafo após inserir arestas (A-B, B-C, A-C, C-D):")
    exibir_grafo(g_matriz, g_vertices)

    print("\n--- Testando Vizinhos ---")
    listar_vizinhos(g_matriz, g_vertices, "C")
    listar_vizinhos(g_matriz, g_vertices, "D")
    listar_vizinhos(g_matriz, g_vertices, "B")

    print("\n--- Testando Percursos Válidos ---")
    caminho1 = ["A", "B", "C", "D"]
    print(f"Caminho {caminho1} é válido? {percurso_valido(g_matriz, g_vertices, caminho1)}")
    
    caminho2 = ["A", "D"]
    print(f"Caminho {caminho2} é válido? {percurso_valido(g_matriz, g_vertices, caminho2)}")
    
    caminho3 = ["D", "C", "A", "B"]
    print(f"Caminho {caminho3} é válido? {percurso_valido(g_matriz, g_vertices, caminho3)}")

    print("\n--- Testando Graus (Não-Direcionado) ---")
    graus = grau_vertices(g_matriz, g_vertices)
    print(json.dumps(graus, indent=2))

    print("\n--- Removendo Aresta (A-C) ---")
    g_matriz, g_vertices = remover_aresta(g_matriz, g_vertices, "A", "C", NAO_DIRECIONADO)
    exibir_grafo(g_matriz, g_vertices)
    print("Vizinhos de 'A' após remoção:")
    listar_vizinhos(g_matriz, g_vertices, "A")

    print("\n--- Removendo Vértice (B) ---")
    g_matriz, g_vertices = remover_vertice(g_matriz, g_vertices, "B")
    exibir_grafo(g_matriz, g_vertices)
    
    print("\n--- Testando Grafo Direcionado ---")
    g2_matriz, g2_vertices = criar_grafo()
    g2_matriz, g2_vertices = inserir_aresta(g2_matriz, g2_vertices, "X", "Y", nao_direcionado=False)
    g2_matriz, g2_vertices = inserir_aresta(g2_matriz, g2_vertices, "Y", "Z", nao_direcionado=False)
    g2_matriz, g2_vertices = inserir_aresta(g2_matriz, g2_vertices, "X", "Z", nao_direcionado=False)
    
    exibir_grafo(g2_matriz, g2_vertices)
    print("Graus (Direcionado):")
    graus_dir = grau_vertices(g2_matriz, g2_vertices)
    print(json.dumps(graus_dir, indent=2))


if __name__ == "__main__":
    main()


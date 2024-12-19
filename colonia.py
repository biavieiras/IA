import numpy as np
import random
import matplotlib.pyplot as plt

# Função para calcular o custo total de uma trajetória
def calcular_trajeto_custo(trajeto, matriz_distancias):
    custo_total = 0
    for i in range(len(trajeto) - 1):
        custo_total += matriz_distancias[trajeto[i]][trajeto[i+1]]
    custo_total += matriz_distancias[trajeto[-1]][trajeto[0]]  # Voltar ao ponto inicial
    return custo_total

# Função para determinar a próxima cidade com base em probabilidades
def selecionar_proxima_parada(atual, opcoes, feromonio, atratividade, peso_feromonio, peso_heuristica):
    pesos = []
    for opcao in opcoes:
        impacto_feromonio = feromonio[atual][opcao] ** peso_feromonio
        impacto_heuristica = atratividade[atual][opcao] ** peso_heuristica
        pesos.append(impacto_feromonio * impacto_heuristica)

    # Normalização dos pesos
    soma_pesos = sum(pesos)
    probabilidades = [peso / soma_pesos for peso in pesos]

    # Seleção baseada nas probabilidades
    return random.choices(opcoes, weights=probabilidades, k=1)[0]

# Implementação do algoritmo baseado em colônia de formigas
def otimizacao_por_formigas(matriz_distancias, qtd_formigas=100, max_iteracoes=1000, peso_feromonio=1.0, peso_heuristica=5.0, taxa_evaporacao=0.1, intensificacao=100):
    n_cidades = len(matriz_distancias)

    # Inicialização das trilhas de feromônio
    trilhas = np.ones((n_cidades, n_cidades))
    atratividade = 1 / (matriz_distancias + 1e-10)  # Heurística inversa da distância

    melhor_trajeto = None
    menor_custo = float('inf')
    historico_custos = []  # Para armazenar o menor custo em cada iteração

    for iteracao in range(max_iteracoes):
        trajetos = []
        custos = []

        # Cada formiga constrói um trajeto
        for _ in range(qtd_formigas):
            trajeto = []
            cidades_disponiveis = list(range(n_cidades))
            cidade_atual = random.choice(cidades_disponiveis)
            trajeto.append(cidade_atual)
            cidades_disponiveis.remove(cidade_atual)

            while cidades_disponiveis:
                proxima_cidade = selecionar_proxima_parada(cidade_atual, cidades_disponiveis, trilhas, atratividade, peso_feromonio, peso_heuristica)
                trajeto.append(proxima_cidade)
                cidades_disponiveis.remove(proxima_cidade)
                cidade_atual = proxima_cidade

            trajetos.append(trajeto)
            custo = calcular_trajeto_custo(trajeto, matriz_distancias)
            custos.append(custo)

            # Atualizar o melhor resultado encontrado
            if custo < menor_custo:
                menor_custo = custo
                melhor_trajeto = trajeto

        # Atualizar trilhas de feromônio
        trilhas *= (1 - taxa_evaporacao)  # Evaporação
        for idx, trajeto in enumerate(trajetos):
            custo = custos[idx]
            for i in range(len(trajeto) - 1):
                trilhas[trajeto[i]][trajeto[i+1]] += intensificacao / custo
            trilhas[trajeto[-1]][trajeto[0]] += intensificacao / custo  # Fechamento do ciclo

        # Armazenar o menor custo desta iteração
        historico_custos.append(menor_custo)

        # Feedback da iteração
        print(f"Iteração {iteracao + 1}: Menor custo = {menor_custo}")

    print("\nMelhor trajeto encontrado:", melhor_trajeto)
    print("Custo do melhor trajeto:", menor_custo)

    # Gerar gráfico de convergência
    plt.figure(figsize=(10, 6))
    plt.plot(historico_custos, label='Menor Custo')
    plt.title('Convergência do Algoritmo de Colônia de Formigas')
    plt.xlabel('Iteração')
    plt.ylabel('Custo')
    plt.legend()
    plt.grid()
    plt.savefig('grafico_colonia_formigas.png')  # Salvar o gráfico como imagem
    plt.show()

    return melhor_trajeto, menor_custo

# Definição da matriz de custos
matriz_distancias = np.array([
    [0, 10, 15, 45, 5, 5, 50, 44, 30, 100, 67, 33, 90, 17, 50],
    [15, 0, 100, 30, 25, 80, 40, 41, 5, 45, 70, 10, 90, 30, 25],
    [40, 80, 0, 90, 70, 33, 100, 70, 30, 23, 80, 60, 47, 33, 25],
    [100, 8, 5, 0, 5, 40, 21, 20, 35, 14, 55, 35, 21, 5, 40],
    [17, 10, 33, 45, 0, 14, 50, 27, 33, 60, 17, 11, 70, 13, 71],
    [15, 70, 90, 11, 0, 35, 80, 11, 18, 35, 15, 90, 23, 50, 23],
    [25, 19, 18, 30, 100, 55, 0, 70, 55, 41, 55, 100, 18, 14, 18],
    [40, 15, 60, 45, 70, 33, 25, 0, 27, 60, 80, 35, 30, 41, 31],
    [21, 34, 17, 10, 18, 21, 8, 32, 0, 47, 76, 21, 90, 21, 41],
    [35, 100, 5, 18, 43, 25, 70, 40, 39, 0, 17, 35, 15, 13, 40],
    [38, 20, 23, 50, 80, 33, 55, 42, 17, 35, 0, 30, 10, 35, 21],
    [15, 14, 45, 21, 100, 10, 8, 20, 35, 43, 8, 0, 15, 30, 10],
    [80, 10, 5, 8, 90, 35, 0, 44, 10, 80, 10, 0, 25, 80, 40],
    [33, 90, 40, 18, 70, 45, 25, 23, 90, 43, 70, 5, 0, 50, 0],
    [25, 70, 45, 50, 5, 45, 20, 100, 25, 50, 35, 10, 90, 5, 0]
])

# Execução do algoritmo com parâmetros ajustados
resultado_trajeto, resultado_custo = otimizacao_por_formigas(matriz_distancias, qtd_formigas=20, max_iteracoes=50)

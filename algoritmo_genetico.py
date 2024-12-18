import numpy as np
import random
import matplotlib.pyplot as plt

# Função para calcular o custo total de um caminho
def calcular_custo(matriz_custos, caminho):
    custo_total = sum(matriz_custos[caminho[i]][caminho[i + 1]] for i in range(len(caminho) - 1))
    custo_total += matriz_custos[caminho[-1]][caminho[0]]  # Retorno à cidade inicial
    return custo_total

# Geração da população inicial
def gerar_populacao_inicial(tamanho_populacao, num_cidades):
    return [random.sample(range(num_cidades), num_cidades) for _ in range(tamanho_populacao)]

# Seleção por torneio
def selecao_torneio(populacao, matriz_custos, k=3):
    return min(random.sample(populacao, k), key=lambda x: calcular_custo(matriz_custos, x))

# Crossover PMX
def crossover_pmx(pai1, pai2):
    tamanho = len(pai1)
    filho = [-1] * tamanho
    p1, p2 = sorted(random.sample(range(tamanho), 2))
    filho[p1:p2+1] = pai1[p1:p2+1]
    for i in range(tamanho):
        if filho[i] == -1:
            valor = pai2[i]
            while valor in filho:
                valor = pai2[pai1.index(valor)]
            filho[i] = valor
    return filho

# Mutação por inversão
def mutacao_inversao(individuo):
    p1, p2 = sorted(random.sample(range(len(individuo)), 2))
    individuo[p1:p2+1] = reversed(individuo[p1:p2+1])
    return individuo

# Algoritmo Genético com Gráfico
def algoritmo_genetico(matriz_custos, tamanho_populacao=100, num_geracoes=1000, probabilidade_mutacao=0.1, k_torneio=3):
    num_cidades = len(matriz_custos)
    populacao = gerar_populacao_inicial(tamanho_populacao, num_cidades)
    melhor_solucao = min(populacao, key=lambda x: calcular_custo(matriz_custos, x))
    melhor_custo = calcular_custo(matriz_custos, melhor_solucao)
    
    historico_custos = []  # Lista para armazenar os custos ao longo das gerações

    for geracao in range(num_geracoes):
        nova_populacao = [melhor_solucao]  # Elitismo
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, matriz_custos, k_torneio)
            pai2 = selecao_torneio(populacao, matriz_custos, k_torneio)
            filho = crossover_pmx(pai1, pai2)
            if random.random() < probabilidade_mutacao:
                filho = mutacao_inversao(filho)
            nova_populacao.append(filho)
        
        populacao = nova_populacao
        candidato = min(populacao, key=lambda x: calcular_custo(matriz_custos, x))
        candidato_custo = calcular_custo(matriz_custos, candidato)
        
        if candidato_custo < melhor_custo:
            melhor_solucao, melhor_custo = candidato, candidato_custo

        # Salva o custo da geração atual
        historico_custos.append(melhor_custo)
        print(f"Geração {geracao+1}: Melhor Custo = {melhor_custo}")

    # Plotando o gráfico de evolução
    plt.figure(figsize=(10, 6))
    plt.plot(historico_custos, color='blue')
    plt.title("Evolução do Custo ao Longo das Gerações")
    plt.xlabel("Gerações")
    plt.ylabel("Custo")
    plt.grid()
    plt.show()
    
    return melhor_solucao, melhor_custo


# Exemplo de execução
if __name__ == "__main__":
    matriz_custos = np.array([
    [0, 10, 15, 45, 5, 45, 50, 44, 30, 100, 67, 33, 90, 17, 50],
    [15, 0, 100, 30, 20, 25, 80, 45, 41, 5, 45, 10, 90, 10, 35],
    [10, 100, 0, 20, 45, 100, 30, 23, 80, 40, 15, 70, 5, 50, 40],
    [100, 8, 5, 0, 5, 40, 21, 20, 35, 14, 55, 35, 21, 5, 40],
    [5, 17, 10, 3, 0, 45, 10, 50, 27, 33, 60, 17, 18, 10, 5],
    [15, 70, 90, 20, 11, 0, 15, 35, 30, 85, 18, 35, 19, 10, 23],
    [25, 19, 18, 30, 5, 100, 0, 70, 55, 41, 55, 100, 18, 41, 35],
    [10, 14, 15, 50, 5, 25, 30, 0, 25, 27, 70, 30, 20, 40, 41],
    [21, 34, 17, 40, 18, 30, 10, 20, 0, 47, 76, 40, 21, 90, 10],
    [35, 100, 5, 18, 10, 8, 35, 20, 33, 0, 14, 70, 35, 45, 21],
    [38, 20, 23, 33, 5, 55, 10, 80, 39, 14, 0, 60, 35, 10, 21],
    [10, 14, 45, 21, 10, 100, 80, 90, 70, 43, 18, 0, 50, 5, 30],
    [33, 80, 10, 5, 18, 75, 25, 44, 10, 70, 30, 50, 0, 25, 10],
    [40, 90, 20, 18, 70, 45, 25, 23, 40, 50, 70, 10, 5, 0, 25],
    [25, 70, 45, 5, 45, 20, 10, 25, 40, 100, 25, 50, 35, 10, 0]
])
    melhor_solucao, melhor_custo = algoritmo_genetico(matriz_custos)
    print(f"\nMelhor solução: {melhor_solucao}")
    print(f"Melhor custo: {melhor_custo}")

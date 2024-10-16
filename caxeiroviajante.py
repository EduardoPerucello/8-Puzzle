import numpy as np
import random
import matplotlib.pyplot as plt

# Função para calcular a distância total de um caminho
def calcular_distancia_total(caminho, pontos):
    distancia = 0
    for i in range(len(caminho)):
        distancia += np.linalg.norm(pontos[caminho[i]] - pontos[caminho[(i + 1) % len(caminho)]])
    return round(distancia, 2)

# Inicialização da população
def inicializar_populacao(pop_size, num_pontos):
    populacao = []
    for _ in range(pop_size):
        individuo = list(range(num_pontos))
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

# Crossover de Ordem (OX)
def cruzamento_ox(pai1, pai2):
    inicio, fim = sorted(random.sample(range(len(pai1)), 2))
    filho = [None] * len(pai1)
    
    # Copia a fatia do pai1
    filho[inicio:fim] = pai1[inicio:fim]
    
    # Preenche o restante com a ordem do pai2
    ptr = fim
    for gene in pai2:
        if gene not in filho:
            if ptr >= len(pai2):
                ptr = 0
            filho[ptr] = gene
            ptr += 1
    return filho

# Mutação por troca de posição
def mutacao_swap(caminho, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(caminho)), 2)
        caminho[i], caminho[j] = caminho[j], caminho[i]
    return caminho

# Seleção por Torneio
def selecionar_torneio(populacao, pontos, k=3):
    selecionados = random.sample(populacao, k)
    selecionados.sort(key=lambda ind: calcular_distancia_total(ind, pontos))
    return selecionados[0]

# Seleção por Roleta
def selecionar_roleta(populacao, pontos):
    fitness = [1 / calcular_distancia_total(ind, pontos) for ind in populacao]
    total_fitness = sum(fitness)
    roleta = [f / total_fitness for f in fitness]
    escolha = random.choices(populacao, weights=roleta, k=1)[0]
    return escolha

# Algoritmo Genético com 100 gerações
def algoritmo_genetico(pontos, pop_size=100, num_geracoes=100, taxa_mutacao=0.2):
    populacao = inicializar_populacao(pop_size, len(pontos))
    melhor_caminho = min(populacao, key=lambda c: calcular_distancia_total(c, pontos))
    melhor_distancia = calcular_distancia_total(melhor_caminho, pontos)

    for geracao in range(num_geracoes):
        nova_populacao = []
        for _ in range(pop_size):
            if random.random() < 0.5:
                pai1 = selecionar_torneio(populacao, pontos)
            else:
                pai1 = selecionar_roleta(populacao, pontos)
            pai2 = selecionar_roleta(populacao, pontos)
            
            filho = cruzamento_ox(pai1, pai2)
            filho = mutacao_swap(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao
        candidato = min(populacao, key=lambda c: calcular_distancia_total(c, pontos))
        candidato_distancia = calcular_distancia_total(candidato, pontos)
        
        # Atualiza o melhor caminho e a melhor distância
        if candidato_distancia < melhor_distancia:
            melhor_caminho = candidato
            melhor_distancia = candidato_distancia

        # Exibição a cada 20 gerações com duas casas decimais
        if (geracao + 1) % 20 == 0:
            print(f"Geração {geracao + 1}: Distância do melhor caminho: {melhor_distancia:.2f}")

    return melhor_caminho, melhor_distancia

# Função para gerar pontos uniformemente distribuídos
def gerar_pontos_uniformemente_distribuidos(num_pontos):
    return np.random.rand(num_pontos, 2) * 10  # Pontos em um espaço 10x10

# Função para gerar pontos em um círculo
def gerar_pontos_em_circulo(num_pontos):
    angulos = np.linspace(0, 2 * np.pi, num_pontos, endpoint=False)
    raio = 5  # Raio do círculo
    x = raio * np.cos(angulos)
    y = raio * np.sin(angulos)
    return np.column_stack((x, y))

# Função para plotar os pontos e o caminho
def plotar_resultado(pontos, caminho):
    plt.figure(figsize=(8, 8))
    plt.scatter(pontos[:, 0], pontos[:, 1], color='blue', label='Pontos')
    
    # Plota o caminho
    caminho_completo = np.append(caminho, caminho[0])  # Para fechar o ciclo
    plt.plot(pontos[caminho_completo, 0], pontos[caminho_completo, 1], color='red', linewidth=2, label='Caminho')

    for i, (x, y) in enumerate(pontos):
        plt.text(x, y, f'{i}', fontsize=12, ha='right')

    plt.title('Resultado do Algoritmo Genético - Problema do Caixeiro Viajante')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(-6, 6)
    plt.ylim(-6, 6)
    plt.axhline(0, color='gray', lw=0.5, ls='--')
    plt.axvline(0, color='gray', lw=0.5, ls='--')
    plt.grid()
    plt.legend()
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    # Cenário 1: Pontos uniformemente distribuídos
    num_pontos_uniformes = random.randint(8, 10)  # Mínimo de 8 pontos
    pontos_uniformes = gerar_pontos_uniformemente_distribuidos(num_pontos_uniformes)
    pontos_uniformes_formatados = np.round(pontos_uniformes, 2)  # Formata os pontos com duas casas decimais
    
    print(f"\nCenário 1: Pontos uniformemente distribuídos")
    print(f"Número de pontos: {num_pontos_uniformes}")
    print("Pontos:\n", pontos_uniformes_formatados)

    melhor_caminho_uniformes, melhor_distancia_uniformes = algoritmo_genetico(pontos_uniformes, pop_size=100, num_geracoes=100, taxa_mutacao=0.3)
    print("\nMelhor caminho após Algoritmo Genético:", melhor_caminho_uniformes)
    print("Distância:", melhor_distancia_uniformes)

    # Plotar o resultado
    plotar_resultado(pontos_uniformes, melhor_caminho_uniformes)

    # Cenário 2: Pontos em um círculo
    num_pontos_circulo = random.randint(8, 10)  # Mínimo de 8 pontos
    pontos_circulo = gerar_pontos_em_circulo(num_pontos_circulo)
    pontos_circulo_formatados = np.round(pontos_circulo, 2)  # Formata os pontos com duas casas decimais
    
    print(f"\nCenário 2: Pontos em um círculo")
    print(f"Número de pontos: {num_pontos_circulo}")
    print("Pontos:\n", pontos_circulo_formatados)

    melhor_caminho_circulo, melhor_distancia_circulo = algoritmo_genetico(pontos_circulo, pop_size=100, num_geracoes=100, taxa_mutacao=0.3)
    print("\nMelhor caminho após Algoritmo Genético:", melhor_caminho_circulo)
    print("Distância:", melhor_distancia_circulo)

    # Plotar o resultado
    plotar_resultado(pontos_circulo, melhor_caminho_circulo)

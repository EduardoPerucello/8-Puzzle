import random
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular a distância euclidiana entre dois pontos
def distancia(ponto1, ponto2):
    return np.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)

# Função de aptidão: Soma das distâncias percorridas no caminho
def fitness(caminho, pontos):
    distancia_total = 0
    for i in range(len(caminho)):
        distancia_total += distancia(pontos[caminho[i]], pontos[caminho[(i + 1) % len(caminho)]])
    return 1 / distancia_total  # Quanto menor a distância, maior o fitness

# Gerar um caminho aleatório (cromossomo)
def gerar_caminho(pontos):
    caminho = list(range(len(pontos)))
    random.shuffle(caminho)
    return caminho

# Seleção por torneio
def selecao(populacao, fitness_pop):
    torneio = random.sample(list(zip(populacao, fitness_pop)), 3)
    torneio.sort(key=lambda x: x[1], reverse=True)  # Ordena pelo melhor fitness
    return torneio[0][0]

# Crossover (Crossover de Ordem - OX)
def crossover(pai1, pai2):
    tamanho = len(pai1)
    filho = [-1] * tamanho
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    # # Definir índices de início e fim fixos
    # inicio = 4  # Índice fixo de início
    # fim = 23    # Índice fixo de fim (exemplo)
    
    filho[inicio:fim] = pai1[inicio:fim]

    for gene in pai2:
        if gene not in filho:
            for i in range(tamanho):
                if filho[i] == -1:
                    filho[i] = gene
                    break
    return filho

# Função para inverter dois pontos adjacentes no caminho e verificar se melhora a distância total
def melhorar_caminho_inversao(caminho, pontos):
    melhorou = False
    for i in range(1, len(caminho) - 1):
        # Calcular a distância atual entre os pontos antes e depois de 'i'
        dist_atual = (distancia(pontos[caminho[i-1]], pontos[caminho[i]]) + 
                      distancia(pontos[caminho[i]], pontos[caminho[i+1]]))
        
        # Calcular a distância se invertermos os pontos 'i' e 'i+1'
        dist_invertida = (distancia(pontos[caminho[i-1]], pontos[caminho[i+1]]) + 
                          distancia(pontos[caminho[i+1]], pontos[caminho[i]]))
        
        # Se a inversão melhorar o caminho, aplica a inversão
        if dist_invertida < dist_atual:
            caminho[i], caminho[i+1] = caminho[i+1], caminho[i]
            melhorou = True
    return caminho, melhorou

# Mutação (Troca de duas cidades e melhoria por inversão)
def mutacao(caminho, taxa_mutacao, pontos):
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(caminho)), 2)
        caminho[i], caminho[j] = caminho[j], caminho[i]
    
    # Aplicar melhoria por inversão se houver ganho
    caminho, melhorou = melhorar_caminho_inversao(caminho, pontos)
    
    return caminho

# Função para criar uma nova geração, incluindo elitismo
def nova_geracao_com_elitismo(populacao, fitness_pop, taxa_mutacao, pontos, elitismo=True):
    nova_populacao = []
    
    if (elitismo):
        # Preservar o melhor indivíduo da geração atual
        melhor_indice = np.argmax(fitness_pop)
        melhor_individuo = populacao[melhor_indice]
        nova_populacao.append(melhor_individuo)
    
    # Preencher o restante da nova população
    for _ in range(len(populacao) - len(nova_populacao)):
        pai1 = selecao(populacao, fitness_pop)
        pai2 = selecao(populacao, fitness_pop)
        filho = crossover(pai1, pai2)
        filho = mutacao(filho, taxa_mutacao, pontos)
        nova_populacao.append(filho)
    
    return nova_populacao

# Função principal do algoritmo genético com elitismo
def algoritmo_genetico(pontos, tamanho_populacao=100, num_geracoes=50, taxa_mutacao=0.08, elitismo=True):
    populacao = [gerar_caminho(pontos) for _ in range(tamanho_populacao)]
    historico_fitness = []

    for geracao in range(num_geracoes):
        fitness_pop = [fitness(caminho, pontos) for caminho in populacao]
        melhor_fitness = max(fitness_pop)
        melhor_caminho = populacao[fitness_pop.index(melhor_fitness)]
        historico_fitness.append(1 / melhor_fitness)

        print(f"Geração {geracao + 1}: Melhor distância: {1 / melhor_fitness}")

        populacao = nova_geracao_com_elitismo(populacao, fitness_pop, taxa_mutacao, pontos, elitismo)

    return melhor_caminho, historico_fitness

# Função para gerar pontos em um círculo
def gerar_pontos_circulares(quantidade, raio=10):
    angulos = np.linspace(0, 2 * np.pi, quantidade, endpoint=False)
    return [(raio * np.cos(angulo), raio * np.sin(angulo)) for angulo in angulos]

# Função para gerar pontos aleatórios (uniformemente distribuídos)
def gerar_pontos_uniformes(quantidade, limite=10):
    return [(random.uniform(-limite, limite), random.uniform(-limite, limite)) for _ in range(quantidade)]

# Plotar os resultados
def plotar_caminho(pontos, caminho, titulo="Caminho"):
    caminho_completo = caminho + [caminho[0]]
    x = [pontos[i][0] for i in caminho_completo]
    y = [pontos[i][1] for i in caminho_completo]
    
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, marker='o')
    plt.title(titulo)
    plt.show()

# Testando com pontos dispostos em círculo
pontos_circulares = gerar_pontos_circulares(25)
melhor_caminho, historico = algoritmo_genetico(pontos_circulares)

plotar_caminho(pontos_circulares, melhor_caminho, "Caminho Circular")

# Testando com pontos aleatórios (uniformemente distribuídos)
pontos_uniformes = gerar_pontos_uniformes(25)
melhor_caminho, historico = algoritmo_genetico(pontos_uniformes)

plotar_caminho(pontos_uniformes, melhor_caminho, "Caminho Uniforme")

# Plotar histórico de fitness (melhor distância ao longo das gerações)
plt.plot(historico)
plt.title("Evolução do Fitness ao Longo das Gerações")
plt.xlabel("Geração")
plt.ylabel("Melhor Distância")
plt.show()

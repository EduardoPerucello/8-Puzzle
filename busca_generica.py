import tkinter as tk
from tkinter import messagebox
import random
from queue import PriorityQueue
from collections import deque

# Variáveis para armazenar os estados e movimentos
historico_movimentos = []  # Lista que guarda o histórico de movimentos
estado_embaralhado_inicial = []  # Estado do quebra-cabeça após o embaralhamento
current_state = []  # Variável global para armazenar o estado atual do puzzle

# Função para verificar o estado final do jogo
def solucao(next_config):
    return next_config == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para mover a peça
def mover_peca(row, col, current_puzzle):
    empty_pos = current_puzzle.index(0)
    espaco_vazio, empty_col = divmod(empty_pos, 3)
    
    if abs(espaco_vazio - row) + abs(empty_col - col) == 1:
        next_config = current_puzzle.copy()
        new_pos = row * 3 + col
        next_config[empty_pos], next_config[new_pos] = next_config[new_pos], next_config[empty_pos]

        estado_antes = [current_puzzle[i:i + 3] for i in range(0, len(current_puzzle), 3)]
        movimento = f"Mover espaço vazio de ({espaco_vazio}, {empty_col}) para ({row}, {col})"
        historico_movimentos.append((estado_antes, movimento))

        return next_config
    return current_puzzle

# Função para atualizar a interface com o estado atual do quebra-cabeça
def update_buttons(current_puzzle):
    for i, button in enumerate(buttons):
        if current_puzzle[i] == 0:
            button.config(text="", state=tk.DISABLED)
        else:
            button.config(text=str(current_puzzle[i]), state=tk.NORMAL)

# Função para embaralhar o quebra-cabeça
def embaralhar_puzzle():
    global estado_embaralhado_inicial, historico_movimentos, current_state
    historico_movimentos.clear()
    while True:
        estado_inicial = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(estado_inicial)
        if eh_resolvivel(estado_inicial):
            global puzzle
            puzzle = estado_inicial
            current_state = puzzle.copy()
            estado_embaralhado_inicial = estado_inicial.copy()
            break

# Função para verificar se o quebra-cabeça é resolvível
def eh_resolvivel(puzzle):
    inversoes = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversoes += 1
    return inversoes % 2 == 0

# Função para reiniciar o jogo para o estado inicial embaralhado
def reiniciar_para_estado_embaralhado():
    global puzzle, current_state
    puzzle = estado_embaralhado_inicial
    current_state = puzzle.copy()
    update_buttons(current_state)

# Função para reiniciar o jogo
def reiniciar_jogo():
    embaralhar_puzzle()
    update_buttons(puzzle)

# Função para imprimir o histórico de movimentos
def print_historico_movimentos():
    print("Histórico de Movimentos:")
    for i, (estado, movimento) in enumerate(historico_movimentos):
        print(f"Movimento {i + 1}: {movimento}")
        for linha in estado:
            print(linha)
        print()

# Função para atualizar o puzzle e os botões
def update_puzzle(row, col):
    global puzzle, current_state
    next_config = mover_peca(row, col, current_state)

    if solucao(next_config):
        puzzle = next_config
        update_buttons(puzzle)
        messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!")
        estado_final = [puzzle[i:i + 3] for i in range(0, len(puzzle), 3)]
        historico_movimentos.append((estado_final, "Puzzle resolvido"))
        print_historico_movimentos()
    else:
        current_state = next_config
        update_buttons(current_state)

# Função para mostrar a solução encontrada
def mostrar_solucao(caminho):
    print("Solução encontrada:")
    for i, estado in enumerate(caminho):
        print(f"Passo {i + 1}:")
        for linha in [estado[i:i + 3] for i in range(0, len(estado), 3)]:
            print(linha)
        print()
    update_buttons(caminho[-1])

# Função auxiliar para gerar os próximos estados
def gerar_proximos_estados(estado):
    proximos_estados = []
    empty_pos = estado.index(0)
    linha_vazia, col_vazia = divmod(empty_pos, 3)

    movimentos = [
        (-1, 0),  
        (1, 0),   
        (0, -1),  
        (0, 1)    
    ]

    for mov_linha, mov_col in movimentos:
        nova_linha = linha_vazia + mov_linha
        nova_coluna = col_vazia + mov_col
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            novo_estado = estado.copy()
            nova_posicao = nova_linha * 3 + nova_coluna
            novo_estado[empty_pos], novo_estado[nova_posicao] = novo_estado[nova_posicao], novo_estado[empty_pos]
            proximos_estados.append((novo_estado, f"Mover para ({nova_linha}, {nova_coluna})"))

    return proximos_estados

# Função para realizar a busca utilizando o método especificado
def busca_generica(tipo_busca):
    global current_state
    # Inicializa a estrutura de dados para a busca com base no tipo especificado
    if tipo_busca == "BFS":
        estrutura = deque()  # Utiliza uma fila para Busca em Largura
    elif tipo_busca == "DFS":
        estrutura = []  # Utiliza uma pilha para Busca em Profundidade
    elif tipo_busca == "A*":
        estrutura = []  # Utiliza uma lista para Busca A*, que será manipulada como uma fila de prioridade
    else:
        raise ValueError("Tipo de busca não reconhecido")  # Se o tipo de busca não for reconhecido, lança uma exceção
    
    # Inicializa a estrutura com o estado inicial do quebra-cabeça
    if tipo_busca == "A*":
        estrutura.append((heuristica_manhattan(current_state), current_state, []))  # Para A*, adiciona a heurística
    else:
        estrutura.append((current_state, []))  # Para BFS e DFS, apenas o estado e o caminho até ele
    
    visitados = set()  # Conjunto para armazenar os estados já visitados
    visitados.add(tuple(current_state))  # Adiciona o estado inicial ao conjunto de visitados
    pais = {tuple(current_state): None}  # Dicionário para armazenar os pais dos estados (para reconstruir o caminho)
    custos = {tuple(current_state): 0} if tipo_busca == "A*" else {}  # Armazena os custos acumulados para A*
    estados_visitados = 0  # Contador para os estados visitados
    
    while estrutura:
        # Retira o próximo estado da estrutura com base no tipo de busca
        if tipo_busca == "DFS":
            estado_atual, caminho = estrutura.pop()  # Para DFS, remove da pilha
        else:
            if tipo_busca == "A*":
                _, estado_atual, caminho = estrutura.pop(0)  # Para A*, remove da fila de prioridade (baseada em heurística)
            else:
                estado_atual, caminho = estrutura.popleft()  # Para BFS, remove da fila
        
        estados_visitados += 1  # Incrementa o contador de estados visitados

        # Verifica se o estado atual é a solução
        if solucao(estado_atual):
            mostrar_solucao(caminho + [estado_atual])  # Mostra a solução encontrada
            print(f"Estados visitados: {estados_visitados}")  # Imprime o número de estados visitados
            return  # Finaliza a busca

        # Gera os próximos estados a partir do estado atual
        for prox_estado, movimento in gerar_proximos_estados(estado_atual):
            if tuple(prox_estado) not in visitados:  # Se o próximo estado ainda não foi visitado
                # Adiciona o próximo estado na estrutura com base no tipo de busca
                if tipo_busca == "A*":
                    estrutura.append((heuristica_manhattan(prox_estado) + len(caminho) + 1, prox_estado, caminho + [estado_atual]))
                else:
                    if tipo_busca == "BFS":
                        estrutura.append((prox_estado, caminho + [estado_atual]))
                    elif tipo_busca == "DFS":
                        estrutura.append((prox_estado, caminho + [estado_atual]))
                visitados.add(tuple(prox_estado))  # Marca o próximo estado como visitado
                pais[tuple(prox_estado)] = estado_atual  # Define o pai do próximo estado
                if tipo_busca == "A*":
                    custos[tuple(prox_estado)] = custos[tuple(estado_atual)] + 1  # Atualiza o custo acumulado para A*

# Heurística de Manhattan para A*
def heuristica_manhattan(estado):
    """
    Calcula a heurística de Manhattan para o estado atual do quebra-cabeça.
    
    A heurística de Manhattan é a soma das distâncias absolutas de cada peça do quebra-cabeça 
    em relação à sua posição correta. A distância de Manhattan é a soma das diferenças absolutas
    das coordenadas horizontais e verticais.

    Parâmetros:
    estado (list): Lista representando o estado atual do quebra-cabeça, onde a peça 0 representa o espaço vazio.

    Retorna:
    int: O valor da heurística de Manhattan para o estado fornecido.
    """
    distancia = 0  # Inicializa a distância total como 0
    
    # Itera sobre as peças do quebra-cabeça, exceto o espaço vazio (0)
    for i in range(1, 9):
        pos_atual = estado.index(i)  # Obtém a posição atual da peça i
        linha_atual, col_atual = divmod(pos_atual, 3)  # Converte a posição linear para coordenadas (linha, coluna)
        
        linha_certa, col_certa = divmod(i - 1, 3)  # Calcula a posição correta (linha, coluna) da peça i
        
        # Calcula a distância de Manhattan entre a posição atual e a posição correta da peça
        distancia += abs(linha_atual - linha_certa) + abs(col_atual - col_certa)
    
    return distancia  # Retorna a soma das distâncias de Manhattan para todas as peças


# Função para iniciar a busca com base no tipo selecionado
def iniciar_busca(tipo_busca):
    busca_generica(tipo_busca)

# Criação da interface gráfica
root = tk.Tk()
root.title("8 Puzzle")
root.configure(bg="lightgray")  # Define a cor de fundo da janela

buttons = []  # Lista para armazenar os botões do quebra-cabeça
puzzle_frame = tk.Frame(root, bg="lightgray")  # Cria um frame para o quebra-cabeça
puzzle_frame.grid(row=0, column=0, columnspan=4)  # Adiciona o frame ao grid

# Criar botões para o quebra-cabeça
for i in range(3):  # Iterar sobre linhas
    for j in range(3):  # Iterar sobre colunas
        botão = tk.Button(puzzle_frame, text="", width=6, height=3,  # Cria um botão
                           font=("Arial", 16, "bold"),
                           bg="purple", fg="white",
                           activebackground="lightgray",
                           command=lambda row=i, col=j: update_puzzle(row, col))  # Define a função de comando para o botão
        botão.grid(row=i, column=j, padx=5, pady=5)  # Adiciona o botão ao grid com espaçamento
        buttons.append(botão)  # Adiciona o botão à lista de botões

# Botões para ações adicionais
tk.Button(root, text="Novo Jogo", command=reiniciar_jogo, width=15, height=2, bg="purple", fg="white").grid(row=1, column=0, padx=10, pady=5)
tk.Button(root, text="Reiniciar", command=reiniciar_para_estado_embaralhado, width=15, height=2, bg="purple", fg="white").grid(row=1, column=1, padx=10, pady=5)

# Botões para iniciar a busca com métodos específicos
tk.Button(root, text="Iniciar BFS", command=lambda: iniciar_busca("BFS"), width=15, height=2, bg="green").grid(row=1, column=2, padx=10, pady=5)
tk.Button(root, text="Iniciar DFS", command=lambda: iniciar_busca("DFS"), width=15, height=2, bg="blue").grid(row=1, column=3, padx=10, pady=5)
tk.Button(root, text="Iniciar A*", command=lambda: iniciar_busca("A*"), width=15, height=2, bg="yellow").grid(row=2, column=1, columnspan=2, padx=10, pady=5)

# Inicialização
reiniciar_jogo()

root.mainloop()

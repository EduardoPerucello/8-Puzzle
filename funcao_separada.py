'''
Itegrantes do grupo:

Beatriz Newman RA: 22002150
Eduardo Perucello RA: 22009978
Gabriel Yamamoto RA: 22003967
Luana Baptista RA: 22006563

'''



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
    # Retorna True se o estado do quebra-cabeça for a solução (1 a 8 e 0 no final)
    return next_config == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para mover a peça
def mover_peca(row, col, current_puzzle):
    empty_pos = current_puzzle.index(0)  # Encontra a posição do espaço vazio
    espaco_vazio, empty_col = divmod(empty_pos, 3)  # Converte a posição linear para coordenadas de linha e coluna

    # Verifica se o movimento é válido (o espaço vazio deve estar adjacente à peça movida)
    if abs(espaco_vazio - row) + abs(empty_col - col) == 1:
        next_config = current_puzzle.copy()  # Cria uma cópia do estado atual
        new_pos = row * 3 + col  # Calcula a nova posição da peça
        # Troca a peça com o espaço vazio
        next_config[empty_pos], next_config[new_pos] = next_config[new_pos], next_config[empty_pos]

        estado_antes = [current_puzzle[i:i + 3] for i in range(0, len(current_puzzle), 3)]  # Formata o estado em uma matriz 3x3
        movimento = f"Mover espaço vazio de ({espaco_vazio}, {empty_col}) para ({row}, {col})"  # Descreve o movimento
        historico_movimentos.append((estado_antes, movimento))  # Adiciona o movimento ao histórico

        return next_config
    return current_puzzle  # Retorna o estado inalterado se o movimento não for válido

# Função para atualizar a interface com o estado atual do quebra-cabeça
def update_buttons(current_puzzle):
    for i, button in enumerate(buttons):
        if current_puzzle[i] == 0:
            button.config(text="", state=tk.DISABLED)  # Desativa o botão para o espaço vazio
        else:
            button.config(text=str(current_puzzle[i]), state=tk.NORMAL)  # Atualiza o texto e ativa o botão

# Função para embaralhar o quebra-cabeça
def embaralhar_puzzle():
    global estado_embaralhado_inicial, historico_movimentos, current_state
    historico_movimentos.clear()  # Limpa o histórico de movimentos
    while True:
        estado_inicial = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Estado inicial do quebra-cabeça
        random.shuffle(estado_inicial)  # Embaralha as peças
        if eh_resolvivel(estado_inicial):  # Verifica se o estado embaralhado é resolvível
            global puzzle
            puzzle = estado_inicial
            current_state = puzzle.copy()  # Atualiza o estado atual
            estado_embaralhado_inicial = estado_inicial.copy()  # Guarda o estado embaralhado inicial
            break

# Função para verificar se o quebra-cabeça é resolvível
def eh_resolvivel(puzzle):
    inversoes = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversoes += 1  # Conta as inversões no quebra-cabeça
    return inversoes % 2 == 0  # Retorna True se o número de inversões for par

# Função para reiniciar o jogo para o estado inicial embaralhado
def reiniciar_para_estado_embaralhado():
    global puzzle, current_state
    puzzle = estado_embaralhado_inicial
    current_state = puzzle.copy()  # Atualiza current_state para o mesmo estado do puzzle
    update_buttons(current_state)  # Atualiza os botões com o estado inicial

# Função para reiniciar o jogo
def reiniciar_jogo():
    embaralhar_puzzle()  # Embaralha o puzzle
    update_buttons(puzzle)  # Atualiza os botões com o novo estado do puzzle

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
    next_config = mover_peca(row, col, current_state)  # Move a peça e obtém o próximo estado

    if solucao(next_config):
        puzzle = next_config
        update_buttons(puzzle)  # Atualiza a interface com o estado resolvido
        messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!")  # Exibe uma mensagem de vitória
        estado_final = [puzzle[i:i + 3] for i in range(0, len(puzzle), 3)]
        historico_movimentos.append((estado_final, "Puzzle resolvido"))  # Adiciona o estado final ao histórico
        print_historico_movimentos()  # Imprime o histórico de movimentos
    else:
        current_state = next_config
        update_buttons(current_state)  # Atualiza a interface com o estado atual

# Função para mostrar a solução encontrada
def mostrar_solucao(caminho):
    print("Solução encontrada:")
    for i, estado in enumerate(caminho):
        print(f"Passo {i + 1}:")
        for linha in [estado[i:i + 3] for i in range(0, len(estado), 3)]:
            print(linha)
        print()
    update_buttons(caminho[-1])  # Atualiza a interface com o estado final da solução

# Função auxiliar para gerar os próximos estados
def gerar_proximos_estados(estado):
    proximos_estados = []
    empty_pos = estado.index(0)  # Encontra a posição do espaço vazio
    linha_vazia, col_vazia = divmod(empty_pos, 3)  # Converte a posição linear para coordenadas de linha e coluna

    movimentos = [
        (-1, 0),  # Cima
        (1, 0),   # Baixo
        (0, -1),  # Esquerda
        (0, 1)    # Direita
    ]

    # Gera os próximos estados baseados em movimentos válidos
    for mov_linha, mov_col in movimentos:
        nova_linha = linha_vazia + mov_linha
        nova_coluna = col_vazia + mov_col
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            novo_estado = estado.copy()
            nova_posicao = nova_linha * 3 + nova_coluna
            novo_estado[empty_pos], novo_estado[nova_posicao] = novo_estado[nova_posicao], novo_estado[empty_pos]
            proximos_estados.append((novo_estado, f"Mover para ({nova_linha}, {nova_coluna})"))

    return proximos_estados

def bfs_solver():
    queue = deque([(current_state, [])])
    visitados = set()  # Usado para evitar ciclos

    estados_visitados = 0

    while queue:
        estados_visitados += 1
        estado_atual, caminho = queue.popleft()

        # Adiciona o estado atual ao caminho
        caminho_atual = caminho + [estado_atual]

        if solucao(estado_atual):
            messagebox.showinfo("8 Puzzle", f"Resolvido com BFS em {estados_visitados} estados visitados!")
            mostrar_solucao(caminho_atual)  # Mostra apenas o caminho correto
            return

        # Gera os próximos estados
        for prox_estado, movimento in gerar_proximos_estados(estado_atual):
            if tuple(prox_estado) not in visitados:
                visitados.add(tuple(prox_estado))  # Marca como visitado para evitar ciclos
                queue.append((prox_estado, caminho_atual))  # Passa o caminho atualizado

    messagebox.showinfo("8 Puzzle", "Sem solução com BFS")


# Busca em profundidade
def dfs_solver(current_state, limite_inicial=2, incremento=2):
    limite = limite_inicial
    while True:
        stack = [(current_state, [], 0)]  # Inicializa a pilha com o estado atual, caminho vazio e profundidade 0
        visitados = set()
        visitados.add(tuple(current_state))  # Marca o estado atual como visitado

        estados_visitados = 0  # Contador para rastrear o número de estados visitados
        encontrou_solucao = False

        while stack:
            estados_visitados += 1
            estado_atual, caminho, profundidade = stack.pop()  # Remove o estado do topo da pilha

            if solucao(estado_atual):
                messagebox.showinfo("8 Puzzle", f"Resolvido com DFS iterativo em {estados_visitados} estados visitados!")
                mostrar_solucao(caminho + [estado_atual])  # Exibe a solução encontrada
                encontrou_solucao = True
                break

            # Se não atingiu o limite de profundidade, continua a busca
            if profundidade < limite:
                # Gera os próximos estados a partir do estado atual
                for prox_estado, movimento in gerar_proximos_estados(estado_atual):
                    if tuple(prox_estado) not in visitados:
                        visitados.add(tuple(prox_estado))  # Marca o próximo estado como visitado
                        stack.append((prox_estado, caminho + [estado_atual], profundidade + 1))  # Adiciona o próximo estado à pilha
        
        if encontrou_solucao:
            break
        
        limite *= incremento  # Incrementa o limite para a próxima iteração

        # Se o limite máximo for atingido e nenhuma solução encontrada
    if not encontrou_solucao:
        messagebox.showinfo("8 Puzzle", "Sem solução com DFS")

# Busca de A*
def astar_solver():
    pq = PriorityQueue()  # Inicializa uma fila de prioridade
    pq.put((heuristica_manhattan(current_state), current_state, []))  # Adiciona o estado inicial à fila de prioridade com custo heurístico
    visitados = set()
    visitados.add(tuple(current_state))  # Marca o estado atual como visitado

    estados_visitados = 0  # Contador para rastrear o número de estados visitados

    while not pq.empty():
        estados_visitados += 1
        _, estado_atual, caminho = pq.get()  # Remove o estado com o menor custo da fila de prioridade

        if solucao(estado_atual):
            messagebox.showinfo("8 Puzzle", f"Resolvido com A* em {estados_visitados} estados visitados!")  # Mensagem de sucesso
            mostrar_solucao(caminho + [estado_atual])  # Exibe a solução encontrada
            return

        # Gera os próximos estados a partir do estado atual
        for prox_estado, movimento in gerar_proximos_estados(estado_atual):
            if tuple(prox_estado) not in visitados:
                visitados.add(tuple(prox_estado))  # Marca o próximo estado como visitado
                custo_est = len(caminho) + 1 + heuristica_manhattan(prox_estado)  # Calcula o custo total para A*
                pq.put((custo_est, prox_estado, caminho + [estado_atual]))  # Adiciona o próximo estado à fila de prioridade

    messagebox.showinfo("8 Puzzle", "Sem solução com A*")  # Mensagem se não encontrar solução

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

# Interface gráfica do jogo
root = tk.Tk()
root.title("8 Puzzle")  # Define o título da janela
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

# Botões de controle
tk.Button(root, text="Novo Jogo", command=reiniciar_jogo, width=15, height=2, bg="purple", fg="white").grid(row=1, column=0, padx=10, pady=5)
tk.Button(root, text="Reiniciar", command=reiniciar_para_estado_embaralhado, width=15, height=2, bg="purple", fg="white").grid(row=1, column=1, padx=10, pady=5)

# Botões de IA com cores específicas e maior tamanho
tk.Button(root, text="Busca Largura", command=bfs_solver, width=15, height=2, bg="green", fg="white").grid(row=1, column=2, padx=10, pady=5)
tk.Button(root, text="Busca Profundidade", command=lambda: dfs_solver(current_state, limite_inicial=2, incremento=2), width=15, height=2, bg="blue", fg="white").grid(row=1, column=3, padx=10, pady=5)
tk.Button(root, text="Busca A*", command=astar_solver, width=15, height=2, bg="yellow", fg="black").grid(row=2, column=1, columnspan=2, padx=10, pady=5)

# Embaralha o puzzle no início
embaralhar_puzzle()
update_buttons(puzzle)

root.mainloop()  # Inicia o loop principal da interface gráfica
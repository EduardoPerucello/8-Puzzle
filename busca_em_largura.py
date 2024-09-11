import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

# Variáveis globais
historico_movimentos = []  # Lista para armazenar o histórico de movimentos
estado_embaralhado_inicial = []  # Estado do quebra-cabeça embaralhado inicial
puzzle = []  # Estado atual do quebra-cabeça
current_state = []  # Estado corrente do quebra-cabeça

# Função de busca genérica, para ser usada com diferentes algoritmos de IA (BFS, DFS, etc.)
def busca_generica(estado_inicial, estrutura):
    estrutura.append(estado_inicial)  # Adiciona o estado inicial na estrutura
    visitados = set()  # Conjunto de estados visitados
    visitados.add(tuple(estado_inicial))
    pais = {tuple(estado_inicial): None}  # Dicionário para rastrear os pais dos estados
    estados_visitados = 0  # Contador de estados visitados

    while estrutura:  # Enquanto houver estados na estrutura
        estado_atual = estrutura.popleft() if isinstance(estrutura, deque) else estrutura.pop()  # Pega o próximo estado
        estados_visitados += 1  # Atualiza o número de estados visitados

        if solucao(estado_atual):  # Verifica se o estado atual é a solução
            passos = []  # Lista para armazenar os passos
            while estado_atual is not None:
                passos.append(estado_atual)
                estado_atual = pais[tuple(estado_atual)]
            passos.reverse()  # Inverte a ordem dos passos para mostrar o caminho correto
            return passos, estados_visitados  # Retorna os passos e o número de estados visitados

        for proximo_estado in gerar_estados_sucessores(estado_atual):
            if tuple(proximo_estado) not in visitados:
                visitados.add(tuple(proximo_estado))
                estrutura.append(proximo_estado)  # Adiciona os estados sucessores na estrutura
                pais[tuple(proximo_estado)] = estado_atual

    return None, estados_visitados  # Retorna None se não houver solução, e o número de estados visitados

# Função para gerar estados sucessores
def gerar_estados_sucessores(estado):
    sucessores = []
    empty_pos = estado.index(0)  # Encontra a posição do espaço vazio
    empty_row, empty_col = divmod(empty_pos, 3)  # Converte a posição em coordenadas de linha e coluna

    # Lista de possíveis movimentos (cima, baixo, esquerda, direita)
    for (row, col) in [(empty_row-1, empty_col), (empty_row+1, empty_col), 
                       (empty_row, empty_col-1), (empty_row, empty_col+1)]:
        if 0 <= row < 3 and 0 <= col < 3:
            next_config = estado.copy()
            new_pos = row * 3 + col
            next_config[empty_pos], next_config[new_pos] = next_config[new_pos], next_config[empty_pos]
            sucessores.append(next_config)
    
    return sucessores

# Função para verificar se o estado é a solução final
def solucao(next_config):
    return next_config == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para atualizar os botões com o estado atual do quebra-cabeça
def update_buttons(current_puzzle):
    for i, button in enumerate(buttons):
        if current_puzzle[i] == 0:
            button.config(text="", state=tk.DISABLED)  # Desativa o botão para o espaço vazio
        else:
            button.config(text=str(current_puzzle[i]), state=tk.NORMAL)

# Função para embaralhar o quebra-cabeça
def embaralhar_puzzle():
    global estado_embaralhado_inicial, historico_movimentos, current_state
    historico_movimentos.clear()
    while True:
        estado_inicial = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(estado_inicial)  # Embaralha o estado inicial
        if e_resolvel(estado_inicial):  # Verifica se o estado é resolvível
            global puzzle
            puzzle = estado_inicial
            current_state = puzzle.copy()
            estado_embaralhado_inicial = estado_inicial.copy()
            break

# Função para verificar se o quebra-cabeça é resolvível
def e_resolvel(puzzle):
    inversoes = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversoes += 1
    return inversoes % 2 == 0

# Função para reiniciar o quebra-cabeça para o estado embaralhado inicial
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
    print("Historico de Movimentos:")
    for i, (estado, movimento) in enumerate(historico_movimentos):
        print(f"Movimento {i + 1}: {movimento}")
        for linha in estado:
            print(linha)
        print()

# Função para mover a peça no quebra-cabeça
def mover_peca(row, col, current_puzzle):
    empty_pos = current_puzzle.index(0)
    empty_row, empty_col = divmod(empty_pos, 3)

    if abs(empty_row - row) + abs(empty_col - col) == 1:  # Verifica se o movimento é válido
        next_config = current_puzzle.copy()
        new_pos = row * 3 + col
        next_config[empty_pos], next_config[new_pos] = next_config[new_pos], next_config[empty_pos]

        estado_antes = [current_puzzle[i:i + 3] for i in range(0, len(current_puzzle), 3)]
        movimento = f"Mover espaco vazio de ({empty_row}, {empty_col}) para ({row}, {col})"
        historico_movimentos.append((estado_antes, movimento))

        return next_config
    return current_puzzle

# Função para atualizar o quebra-cabeça após um movimento
def update_puzzle(row, col):
    global puzzle, current_state
    next_config = mover_peca(row, col, current_state)

    if solucao(next_config):
        puzzle = next_config
        update_buttons(puzzle)
        messagebox.showinfo("8 Puzzle", "Parabens, voce ganhou!!!")
        estado_final = [puzzle[i:i + 3] for i in range(0, len(puzzle), 3)]
        historico_movimentos.append((estado_final, "Puzzle resolvido"))
        print_historico_movimentos()
    else:
        current_state = next_config
        update_buttons(current_state)

# Função para resolver o quebra-cabeça com Busca em Largura (BFS)
def resolver_com_bfs():
    global puzzle
    estrutura = deque()  # Utiliza deque como fila para BFS
    resultado, estados_visitados = busca_generica(puzzle, estrutura)
    
    if resultado is None:
        messagebox.showinfo("8 Puzzle", "Não foi possível encontrar uma solução.")
    else:
        for passo in resultado:
            update_buttons(passo)
            root.update_idletasks()
            root.after(500)  # Atraso para visualização dos passos
        messagebox.showinfo("8 Puzzle", f"Solução encontrada com Busca em Largura. Estados visitados: {estados_visitados}")
        print_historico_movimentos()  # Imprimir todos os movimentos do algoritmo

# Criar a interface gráfica
root = tk.Tk()
root.title("8 Puzzle")
root.configure(bg="lightgray")
buttons = []

frame = tk.Frame(root, padx=10, pady=10, bg="lightgray")
frame.pack()

# Criar os botões para o quebra-cabeça
for i in range(3):
    for j in range(3):
        botao = tk.Button(frame, text="", width=6, height=3,
                          font=("Arial", 16, "bold"),
                          bg="purple", fg="white",
                          activebackground="lightgray",
                          command=lambda row=i, col=j: update_puzzle(row, col))
        botao.grid(row=i, column=j, padx=5, pady=5)
        buttons.append(botao)


# Criar os botões de controle
control_frame = tk.Frame(root, pady=10, bg="lightgray")
control_frame.pack()

reinicia_botao = tk.Button(control_frame, text="Novo Jogo", command=reiniciar_jogo, font=("Arial", 12, "bold"), bg="purple", fg="white")
reinicia_botao.grid(row=0, column=0, padx=5)

restaurar_estado_botao = tk.Button(control_frame, text="Reiniciar", command=reiniciar_para_estado_embaralhado, font=("Arial", 12, "bold"), bg="purple", fg="white")
restaurar_estado_botao.grid(row=0, column=1, padx=5)

resolver_botao = tk.Button(control_frame, text="Resolver com BFS", command=resolver_com_bfs, font=("Arial", 12, "bold"), bg="purple", fg="white")
resolver_botao.grid(row=0, column=2, padx=5)

reiniciar_jogo()

root.mainloop()

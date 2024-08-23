import tkinter as tk
from tkinter import messagebox
import random

# Variáveis para armazenar os estados e movimentos
historico_movimentos = []
estado_embaralhado_inicial = []

# Função para verificar o estado final do jogo
def solução(next_config):
    return next_config == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para mover a peça
def mover_peça(row, col, current_puzzle):
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
        if é_resolvível(estado_inicial):
            global puzzle
            puzzle = estado_inicial
            current_state = puzzle.copy()
            estado_embaralhado_inicial = estado_inicial.copy()
            break

# Função para verificar se o quebra-cabeça é resolvível
def é_resolvível(puzzle):
    inversões = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversões += 1
    return inversões % 2 == 0

# Função para reiniciar o jogo para o estado inicial embaralhado
def reiniciar_para_estado_embaralhado():
    global puzzle, current_state
    puzzle = estado_embaralhado_inicial
    current_state = puzzle.copy()  # Atualiza current_state para o mesmo estado do puzzle
    update_buttons(current_state)  # Atualiza os botões com o estado inicial

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
    next_config = mover_peça(row, col, current_state)

    if solução(next_config):
        puzzle = next_config
        update_buttons(puzzle)
        messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!")
        estado_final = [puzzle[i:i + 3] for i in range(0, len(puzzle), 3)]
        historico_movimentos.append((estado_final, "Puzzle resolvido"))
        print_historico_movimentos()
    else:
        current_state = next_config
        update_buttons(current_state)

# Criar a interface
root = tk.Tk()
root.title("8 Puzzle")
root.configure(bg="lightgray")
buttons = []

frame = tk.Frame(root, padx=10, pady=10, bg="lightgray")
frame.pack()

for i in range(3):
    for j in range(3):
        botão = tk.Button(frame, text="", width=6, height=3,
                          font=("Arial", 16, "bold"),
                          bg="purple", fg="white",
                          activebackground="lightgray",
                          command=lambda row=i, col=j: update_puzzle(row, col))
        botão.grid(row=i, column=j, padx=5, pady=5)
        buttons.append(botão)

control_frame = tk.Frame(root, pady=10, bg="lightgray")
control_frame.pack()

reinicia_botão = tk.Button(control_frame, text="Novo Jogo", command=reiniciar_jogo, font=("Arial", 12, "bold"), bg="purple", fg="white")
reinicia_botão.grid(row=0, column=0, padx=5)

restaurar_estado_botão = tk.Button(control_frame, text="Reiniciar", command=reiniciar_para_estado_embaralhado, font=("Arial", 12, "bold"), bg="purple", fg="white")
restaurar_estado_botão.grid(row=0, column=1, padx=5)

reiniciar_jogo()

root.mainloop()

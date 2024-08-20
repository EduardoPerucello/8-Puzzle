import tkinter as tk
from tkinter import messagebox
import random

# Função para verificar o estado final do jogo
def solução(puzzle):
    return puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para mover uma peça
def mover_peça(row, col):
    empty_pos = puzzle.index(0) # Encontra a posição do espaço vazio no quebra-cabeça
    empty_row, empty_col = divmod(empty_pos, 3) # Converte a posição linear do espaço vazio para coordenadas de linha e coluna na grade 3x3
    
    if abs(empty_row - row) + abs(empty_col - col) == 1: # Verifica se a peça clicada está adjacente ao espaço vazio
        new_pos = row * 3 + col # Calcula a nova posição linear da peça que será movida
        puzzle[empty_pos], puzzle[new_pos] = puzzle[new_pos], puzzle[empty_pos] # Troca a peça com o espaço vazio
        update_buttons() # Atualiza os botões com o novo estado do quebra-cabeça
        if solução(puzzle): # Verifica se o quebra-cabeça está na solução final
            messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!") # Mostra uma mensagem de vitória

# Função para atualizar a interface com o estado atual do quebra-cabeça
def update_buttons():
    for i, button in enumerate(buttons): # Itera sobre cada botão
        if puzzle[i] == 0: # Se o valor do quebra-cabeça é 0 (espaço vazio)
            button.config(text="", state=tk.DISABLED) # Desativa o botão e limpa o texto
        else:
            button.config(text=str(puzzle[i]), state=tk.NORMAL) # Atualiza o texto do botão com o número da peça

# Função para embaralhar o quebra-cabeça
def embaralhar_puzzle():
    global puzzle
    # puzzle = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    while True:
        puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8] # Configuração inicial do quebra-cabeça
        random.shuffle(puzzle) # Embaralha a lista de peças
        if é_resolvível(puzzle): # Verifica se a configuração embaralhada é resolvível
            break # Sai do loop se a configuração for resolvível

# Função para verificar se o quebra-cabeça é resolvível
def é_resolvível(puzzle):
    inversões = 0
    for i in range(len(puzzle)): # Itera sobre cada peça
        for j in range(i + 1, len(puzzle)): # Compara com as peças subsequentes
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]: # Conta inversões
                inversões += 1
    return inversões % 2 == 0 # Retorna True se o número de inversões for par

# Função para reiniciar o jogo
def reiniciar_jogo():
    embaralhar_puzzle() # Embaralha o quebra-cabeça
    update_buttons() # Atualiza os botões com o novo estado do quebra-cabeça

# Criar a interface
root = tk.Tk()
root.title("8 Puzzle")

puzzle = [] # Lista para armazenar o estado atual do quebra-cabeça
buttons = [] # Lista para armazenar os botões do quebra-cabeça

frame = tk.Frame(root, padx=10, pady=10) # Cria um frame para os botões
frame.pack()

# Criar botões para o quebra-cabeça
for i in range(3):  # Iterar sobre linhas
    for j in range(3):  # Iterar sobre colunas
        botão = tk.Button(frame, text="", width=6, height=3, # Cria um botão
                           font=("Arial", 16, "bold"),
                           bg="purple", fg="white",
                           command=lambda row=i, col=j: mover_peça(row, col)) # Define a função de comando para o botão
        botão.grid(row=i, column=j, padx=5, pady=5) # Adiciona o botão ao grid
        buttons.append(botão) # Adiciona o botão à lista de botões

# Adicionar botão de reinício
reinicia_botão = tk.Button(root, text="Reiniciar", command=reiniciar_jogo, font=("Arial", 12, "bold")) # Cria o botão de reinício
reinicia_botão.pack(pady=10) # Adiciona o botão de reinício ao layout

reiniciar_jogo()  # Configuração inicial do quebra-cabeça

root.mainloop() # Inicia o loop principal da interface

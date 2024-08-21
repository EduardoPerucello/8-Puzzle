import tkinter as tk
from tkinter import messagebox
import random

# Variável para armazenar os estados e movimentos
historico_movimentos = []

# Função para verificar o estado final do jogo
def solução(puzzle):
    return puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Função para mover uma peça
def mover_peça(row, col):
    empty_pos = puzzle.index(0)  # Encontra a posição do espaço vazio no quebra-cabeça
    espaco_vazio, empty_col = divmod(empty_pos, 3)  # Converte a posição linear do espaço vazio para coordenadas de linha e coluna na grade 3x3

    if abs(espaco_vazio - row) + abs(empty_col - col) == 1:  # Verifica se a peça clicada está adjacente ao espaço vazio
        
        # Armazena o estado atual e o movimento realizado antes da troca (Salva o estado como matriz e o formato de impressão 
        estado_antes = [puzzle[i:i + 3] for i in range(0, len(puzzle), 3)] 
        movimento = f"Mover espaço vazio de ({espaco_vazio}, {empty_col}) para ({row}, {col})"
        historico_movimentos.append((estado_antes, movimento))

        # Executa a troca e atualiza os botões com o novo estado do quebra-cabeça
       
        new_pos = row * 3 + col 
        puzzle[empty_pos], puzzle[new_pos] = puzzle[new_pos], puzzle[empty_pos] 
        update_buttons()  

        if solução(puzzle):
            messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!")  
            print_historico_movimentos()

# Função para atualizar a interface com o estado atual do quebra-cabeça
def update_buttons():
    for i, button in enumerate(buttons):  # Itera sobre cada botão
        if puzzle[i] == 0:  # Se o valor do quebra-cabeça é 0 (espaço vazio)
            button.config(text="", state=tk.DISABLED)  # Desativa o botão e limpa o texto
        else:
            button.config(text=str(puzzle[i]), state=tk.NORMAL)  # Atualiza o texto do botão com o número da peça

# Função para embaralhar o quebra-cabeça
def embaralhar_puzzle():
    global puzzle, historico_movimentos
    historico_movimentos.clear()  # Limpa o histórico de movimentos ao reiniciar o jogo
    while True:
        estado_inicial = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(estado_inicial)  # Embaralha a lista de peças
        if é_resolvível(estado_inicial):  # Verifica se a configuração embaralhada é resolvível
            puzzle = estado_inicial
            break  # Sai do loop se a configuração for resolvível

# Função para verificar se o quebra-cabeça é resolvível
def é_resolvível(puzzle):
    inversões = 0
    for i in range(len(puzzle)):  # Itera sobre cada peça
        for j in range(i + 1, len(puzzle)):  # Compara com as peças subsequentes
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:  # Conta inversões
                inversões += 1
    return inversões % 2 == 0  # Retorna True se o número de inversões for par

# Função para reiniciar o jogo
def reiniciar_jogo():
    embaralhar_puzzle()  # Embaralha o quebra-cabeça
    update_buttons()  # Atualiza os botões com o novo estado do quebra-cabeça

# Função para imprimir o histórico de movimentos
def print_historico_movimentos():
    print("Histórico de Movimentos:")
    for i, (estado, movimento) in enumerate(historico_movimentos):
        print(f"Movimento {i + 1}: {movimento}")
        for linha in estado:
            print(linha)
        print()

# Criar a interface
root = tk.Tk()
root.title("8 Puzzle")
buttons = []  # Lista para armazenar os botões do quebra-cabeça

frame = tk.Frame(root, padx=10, pady=10)  # Cria um frame para os botões
frame.pack()

# Criar botões para o quebra-cabeça
for i in range(3):  # Iterar sobre linhas
    for j in range(3):  # Iterar sobre colunas
        botão = tk.Button(frame, text="", width=6, height=3,  # Cria um botão
                        font=("Arial", 16, "bold"),
                        bg="purple", fg="white",
                        command=lambda row=i, col=j: mover_peça(row, col))  # Define a função de comando para o botão
        botão.grid(row=i, column=j, padx=5, pady=5)  # Adiciona o botão ao grid
        buttons.append(botão)  # Adiciona o botão à lista de botões

# Adicionar botão de reinício
reinicia_botão = tk.Button(root, text="Reiniciar", command=reiniciar_jogo, font=("Arial", 12, "bold"))  # Cria o botão de reinício
reinicia_botão.pack(pady=10)  # Adiciona o botão de reinício ao layout

reiniciar_jogo()  # Configuração inicial do quebra-cabeça

root.mainloop()  # Inicia o loop principal da interface

import tkinter as tk
from tkinter import messagebox

# Função para verificar o estado final do jogo
def solução(puzzle):
    return puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 0]



# Função para mover uma peça (acho que está errada essa função)
def mover_peça(row, col):
    empty_pos = puzzle.index(0) # encontra a posição do espaço vazio no quebra-cabeça
    empty_row, empty_col = divmod(empty_pos, 3) # Converte a posição linear do espaço vazio para coordenadas de linha e coluna na grade 3x3. quociente é a linha e o resto é a coluna do espaço vazio 
    
    if abs(empty_row - row) + abs(empty_col - col) == 1: #Verifica se a peça clicada está adjacente ao espaço vazio.
        new_pos = row * 3 + col
        puzzle[empty_pos], puzzle[new_pos] = puzzle[new_pos], puzzle[empty_pos]
        update_buttons()
        if solução(puzzle):
            messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!")

# Função para atualizar a interface com o estado atual do quebra-cabeça
def update_buttons():
    for i, button in enumerate(buttons):
        if puzzle[i] == 0:
            button.config(text="", state=tk.DISABLED)
        else:
            button.config(text=str(puzzle[i]), state=tk.NORMAL)

# Configuração inicial do quebra-cabeça (futuramente mudar para aleatório)
def reiniciar_jogo():
    global puzzle
    puzzle = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    update_buttons()

# Criar a interface
root = tk.Tk()
root.title("8 Puzzle")

puzzle = []
buttons = []

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Criar botões para o quebra-cabeça
for i in range(3):  # Iterar sobre linhas
    for j in range(3):  # Iterar sobre colunas
        botão = tk.Button(frame, text="", width=6, height=3,
                           font=("Arial", 16, "bold"),
                           bg="purple", fg="white",
                           command=lambda row=i, col=j: mover_peça(row, col))
        botão.grid(row=i, column=j, padx=5, pady=5)
        buttons.append(botão)

# Adicionar botão de reinício
reinicia_botão = tk.Button(root, text="Reiniciar", command=reiniciar_jogo, font=("Arial", 12, "bold"))
reinicia_botão.pack(pady=10)

reiniciar_jogo()  # Configuração inicial do quebra-cabeça

root.mainloop()
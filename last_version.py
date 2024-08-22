import tkinter as tk
from tkinter import messagebox
import random

# Variáveis para armazenar os estados e movimentos
historico_movimentos = []
estado_embaralhado_inicial = []  # Adiciona uma variável para armazenar o estado inicial embaralhado

# Função para verificar o estado final do jogo
def solução(next_config):
    return next_config == [1, 2, 3, 4, 5, 6, 7, 8, 0]

def mover_peça(row, col, current_puzzle):
    empty_pos = current_puzzle.index(0)  # Encontra a posição do espaço vazio no quebra-cabeça
    espaco_vazio, empty_col = divmod(empty_pos, 3)  # Converte a posição linear do espaço vazio para coordenadas de linha e coluna na grade 3x3

    if abs(espaco_vazio - row) + abs(empty_col - col) == 1:  # Verifica se a peça clicada está adjacente ao espaço vazio
        # Cria uma cópia do puzzle atual para não modificar o original
        next_config = current_puzzle.copy()

        # Executa a troca na cópia
        new_pos = row * 3 + col 
        next_config[empty_pos], next_config[new_pos] = next_config[new_pos], next_config[empty_pos]

        # Armazena o estado atual e o movimento realizado antes da troca
        estado_antes = [current_puzzle[i:i + 3] for i in range(0, len(current_puzzle), 3)] 
        movimento = f"Mover espaço vazio de ({espaco_vazio}, {empty_col}) para ({row}, {col})"
        historico_movimentos.append((estado_antes, movimento))

        update_buttons(next_config)  

        if solução(next_config):
            estado_final = [next_config[i:i + 3] for i in range(0, len(next_config), 3)]
            historico_movimentos.append((estado_final, "Puzzle resolvido"))
            print_historico_movimentos()
            messagebox.showinfo("8 Puzzle", "Parabéns, você ganhou!!!")



        return next_config  # Retorna a nova configuração

    return current_puzzle  # Retorna o puzzle atual se a peça não puder ser movida

# Função para atualizar a interface com o estado atual do quebra-cabeça
def update_buttons(current_puzzle):
    for i, button in enumerate(buttons):  # Itera sobre cada botão
        if current_puzzle[i] == 0:  # Se o valor do quebra-cabeça é 0 (espaço vazio)
            button.config(text="", state=tk.DISABLED)  # Desativa o botão e limpa o texto
        else:
            button.config(text=str(current_puzzle[i]), state=tk.NORMAL)  # Atualiza o texto do botão com o número da peça

# Função para embaralhar o quebra-cabeça
def embaralhar_puzzle():
    global estado_embaralhado_inicial, historico_movimentos
    historico_movimentos.clear()  # Limpa o histórico de movimentos ao reiniciar o jogo
    while True:
        estado_inicial = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(estado_inicial)  # Embaralha a lista de peças
        if é_resolvível(estado_inicial):  # Verifica se a configuração embaralhada é resolvível
            global puzzle
            puzzle = estado_inicial
            estado_embaralhado_inicial = estado_inicial.copy()  # Armazena o estado embaralhado inicial
            break  # Sai do loop se a configuração for resolvível

# Função para verificar se o quebra-cabeça é resolvível
def é_resolvível(puzzle):
    inversões = 0
    for i in range(len(puzzle)):  # Itera sobre cada peça
        for j in range(i + 1, len(puzzle)):  # Compara com as peças subsequentes
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:  # Conta inversões
                inversões += 1
    return inversões % 2 == 0  # Retorna True se o número de inversões for par

# Função para reiniciar o jogo para o estado inicial embaralhado
def reiniciar_para_estado_embaralhado():
    global puzzle
    puzzle = estado_embaralhado_inicial  # Restaura o estado embaralhado inicial
    update_buttons(puzzle)  # Atualiza os botões com o estado inicial

# Função para reiniciar o jogo
def reiniciar_jogo():
    embaralhar_puzzle()  # Embaralha o quebra-cabeça
    update_buttons(puzzle)  # Atualiza os botões com o novo estado do quebra-cabeça

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
    global puzzle
    puzzle = mover_peça(row, col, puzzle)  # Atualiza o puzzle com o retorno da função mover_peça
    update_buttons(puzzle)  # Atualiza os botões com o estado atual

# Criar a interface
root = tk.Tk()
root.title("8 Puzzle")
root.configure(bg="lightgray")  # Define a cor de fundo da janela principal
buttons = []  # Lista para armazenar os botões do quebra-cabeça

frame = tk.Frame(root, padx=10, pady=10, bg="lightgray")  # Cria um frame para os botões do quebra-cabeça com fundo lightgray
frame.pack()

# Criar botões para o quebra-cabeça
for i in range(3):  # Iterar sobre linhas
    for j in range(3):  # Iterar sobre colunas
        botão = tk.Button(frame, text="", width=6, height=3,  # Cria um botão
                        font=("Arial", 16, "bold"),
                        bg="purple", fg="white",  # Define a cor de fundo dos botões e a cor do texto
                        activebackground="lightgray",
                        command=lambda row=i, col=j: update_puzzle(row, col))  # Passa o estado atual do puzzle
        botão.grid(row=i, column=j, padx=5, pady=5)  # Adiciona o botão ao grid
        buttons.append(botão)  # Adiciona o botão à lista de botões

# Criar um frame para os botões de controle
control_frame = tk.Frame(root, pady=10, bg="lightgray")  # Cria um frame para os botões de controle com fundo lightgray
control_frame.pack()

# Adicionar botões de controle ao frame
reinicia_botão = tk.Button(control_frame, text="Novo Jogo", command=reiniciar_jogo, font=("Arial", 12, "bold"), bg="purple", fg="white")  # Cria o botão de reinício
reinicia_botão.grid(row=0, column=0, padx=5)  # Adiciona o botão ao grid

restaurar_estado_botão = tk.Button(control_frame, text="Reiniciar", command=reiniciar_para_estado_embaralhado, font=("Arial", 12, "bold"), bg="purple", fg="white")  # Cria o botão para restaurar estado embaralhado
restaurar_estado_botão.grid(row=0, column=1, padx=5)  # Adiciona o botão ao grid

reiniciar_jogo()  # Configuração inicial do quebra-cabeça

root.mainloop()  # Inicia o loop principal da interface
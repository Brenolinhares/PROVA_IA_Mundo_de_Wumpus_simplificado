# Prova 3 -IA - Questao 4
# Aluno: Breno Linhares de Sousa- 170007057
# Codigo modificado de : https://github.com/alexander-bachmann/wumpus-world

# Arquivo: agent.py reponsavel por criar a janela grafica com botoes de interacao com os mundos de Wumpus com definições disponi­vel em World_n.txt

# imrportacao de modulos

from tkinter import *
from q_4_agent import Agent
from q_4_world import World
from q_4_grid_label import Grid_Label
import time


def solve_wumpus_world(master, world_file): # Geracao do mundo de wumpus
    world = World()
    world.generate_world(world_file) # Geracao do mundo de wumpus
    label_grid = [[Grid_Label(master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)] # definição do numero de linhas e colunas da grade
    agent = Agent(world, label_grid)

    # Solucao do Agente
    while agent.exited == False: 
        agent.explore()              # explora a caverna ao sair da posicao inicial
        if agent.found_gold == True: # se o agente encontrar o ouro
           break # (NAO PRECISA RETORNAR)
  
    agent.repaint_world() # mudancas nos blocos apos a realizacao da acao ou suposicao
    agent.world_knowledge[agent.world.agent_row][agent.world.agent_col].remove('A')
    time.sleep(1.5)       # tempo de atualizacao de acoes nos quadrados
    agent.repaint_world()


master = Tk()
master.title("Wumpus World-Simplificado") # Titulo da janela

world = World()
world.generate_world("Fase_1.txt") # indica o arquivo que contem o posicionamento dos elementos do mundo
label_grid = [[Grid_Label(master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]

# Configuracao Inicial do Mundo de Wumpus definido no arquivo "Fase_n.txt"

world_1 = Button(master, text="Fase 1",  command= lambda: solve_wumpus_world(master, "Fase_1.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world_2 = Button(master, text="Fase 2",  command= lambda: solve_wumpus_world(master, "Fase_2.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world_3 = Button(master, text="Fase 3",  command= lambda: solve_wumpus_world(master, "Fase_3.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world_4 = Button(master, text="Fase 4",  command= lambda: solve_wumpus_world(master, "Fase_4.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")


#coloca opções para selecionar o mundo na janela
world_1.grid(row = 0, column = len(label_grid[0]))
world_2.grid(row = 1, column = len(label_grid[0]))
world_3.grid(row = 2, column = len(label_grid[0]))
world_4.grid(row = 3, column = len(label_grid[0]))


mainloop()

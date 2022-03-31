# Prova 3 -IA - Questao 4
# Aluno: Breno Linhares de Sousa- 170007057
# Codigo modificado de : https://github.com/alexander-bachmann/wumpus-world

#Arquivo grid_label.py: cria a grade com formatacoes desejadas de tamanho,cor , fonte, numero de linhas e colunas dos elementos da janela


from tkinter import *

class Grid_Label():
    def __init__(self, master, i, j):
        self.text = StringVar()
        self.label = Label(master, textvariable = self.text, height = 5, width = 11, relief = RIDGE, bg = "gray30", fg = "blue", font = "Helvetica 14 bold")
        self.label.grid(row = i, column = j, sticky = W, pady = 1)
        self.row = i # linha da grade
        self.col = j # coluna da grade 
    def change_text(self, updated_text): # atualizacao de textos na janela
        self.text.set(str(updated_text))

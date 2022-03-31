# Prova 3 -IA - Questao 4
# Aluno: Breno Linhares de Sousa- 170007057
# Codigo modificado de : https://github.com/alexander-bachmann/wumpus-world

#Arquivo: Gera o mundo com os elementos iniciais


from q_4_file_parser import File_Parser


class World:
    def __init__(self):
        self.world = [[]]
        self.num_rows = 0 # valor inicial para linha
        self.num_cols = 0 # valor inicial para coluna

        self.agent_row = 0 # linha inicial do agente
        self.agent_col = 0 # coluna inicial do agente
        self.cave_entrance_row = 0 # linha de entrada da caverna
        self.cave_entrance_col = 0 # coluna de entrada da caverna


    def generate_world(self, file_name):

        file_parser = File_Parser(file_name) # puxa os demais arquivos que fazem parte do programa
        
       # Arquivos puxados a serem utilizados: 
        """
        print(file_parser.row_col)
        print(file_parser.agent)
        print(file_parser.wumpus)
        print(file_parser.gold)
        print(file_parser.pits)
        """
        self.num_rows = int(file_parser.row_col[0])
        self.num_cols = int(file_parser.row_col[1])

        self.world = [[[] for i in range(self.num_cols)] for j in range(self.num_rows)] # pecorre linhas e colunas

        self.agent_row = int(file_parser.agent[1])
        self.agent_col = int(file_parser.agent[2])
        self.world[self.agent_row][self.agent_col].append('A')


        
        self.world[int(file_parser.gold[1])][int(file_parser.gold[2])].append(file_parser.gold[0])
        for pit in file_parser.pits:
            self.world[int(pit[1])][int(pit[2])].append(pit[0])


        self.populate_indicators()

    def populate_indicators(self): # funcao que popula(adiciona) elementos no mapa (mundo de wumpus)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                for k in range(len(self.world[i][j])):
                  
                    if self.world[i][j][k] == 'G':
                        print("Gold at [" + str(i) + ", " + str(j) + "]")
                    

                    if self.world[i][j][k] == 'P': # se temos um poco e marcado que possui uma brisa (B) nos quadrados proximos ao poco
                        

                        try:
                            if i-1 >= 0:
                                if 'B' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('B') # se tiver poco marca a brisa que pode esta ao redor do poco
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols:
                                if 'B' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('B') # se tiver poco marca a brisa que pode esta ao redor do poco
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows:
                                if 'B' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('B') # se tiver poco marca a brisa que pode esta ao redor do poco
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'B' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('B')# se tiver poco marca a brisa que pode esta ao redor do poco
                        except IndexError:
                            pass

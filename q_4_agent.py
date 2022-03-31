# Prova 3 -IA - Questao 4
# Aluno: Breno Linhares de Sousa- 170007057
# Código modificado de : https://github.com/alexander-bachmann/wumpus-world

#Arquivo agent.py: Realiza a descricao do agente, quais sao suas possiveis acoes, e a base de conhecimento KB(knowledg base) que o agente possui.

"""
Legend:
. = visited tile
A = agent
G = gold
W = wumpus
S = stench
w = potential wumpus
nw = no wumpus
P = pit
B = breeze
p = potential pit
np = no pit
"""

import time

class Agent:
    def __init__(self, world, label_grid):
        self.world = world                   # Cria o mundo 
        self.world_knowledge = [[[] for i in range(self.world.num_cols)] for j in range(self.world.num_rows)]
        self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A') # cria base de conhecimento
        self.num_stenches = 0
        self.path_out_of_cave = [[self.world.agent_row, self.world.agent_col]] # faz amazenamento do caminho para sair da caverna
        self.mark_tile_visited()                            # marca quadrados visitados
        self.world.cave_entrance_row = self.world.agent_row # posicao inicial de entrada da caverna (Linha)
        self.world.cave_entrance_col = self.world.agent_col # posicao inicial de entrada da caverna (Coluna)
        self.found_gold = False 
        self.took_gold = False # caso o ouro ainda nao tenha sido levado
        self.exited = False    # caso nao tenha saido da caverna 
        self.label_grid = label_grid

        self.repaint_world()
      

    def repaint_world(self): # Esta funcao marca o mundo (quadrados) com as informacoes encontradas e deduzidas pelo agente
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols): # percorre linhas e colunas na grade 4x4
                updated_text = []
                if 'A' in self.world_knowledge[i][j]:
                    updated_text.append('A')         # Marca o quadrado onde se encontra o agente
                    
                if 'p' in self.world_knowledge[i][j]:
                    updated_text.append('P')         # poco
                    
                if 'B' in self.world_knowledge[i][j]:
                    updated_text.append('B')         # Marca o quadrado onde se encontra o Briza
               
                if 'G' in self.world_knowledge[i][j]:
                    updated_text.append('G')         # Marca o quadrado onde se encontra o ouro

                updated_str=""

                self.label_grid[i][j].change_text(updated_str.join(updated_text))
                if '.' in self.world_knowledge[i][j]:
                    self.label_grid[i][j].label.config(bg="gray40")
                self.label_grid[i][j].label.update()
 

    def go_back_one_tile(self): # Funcao com algumas definicoes de acoes(movimento) do agente
        
        # Indica as direcoes a serem tomadas para o  caminho realizado na caverna
        if self.world.agent_row-1 == self.path_out_of_cave[-1][0]:
            self.move('u')
        if self.world.agent_row+1 == self.path_out_of_cave[-1][0]:
            self.move('d')
        if self.world.agent_col+1 ==  self.path_out_of_cave[-1][1]:
            self.move('r')
        if self.world.agent_col-1 ==  self.path_out_of_cave[-1][1]:
            self.move('l')


        del self.path_out_of_cave[-1]

    def explore(self): # Funcao que define acoes para a exploracao da caverna
        last_move = ''
        already_moved = False # se o agente nao esta se movendo
        while self.found_gold == False:  # enquanto nao encontrar o ouro

            if self.found_gold == True:  # caso o ouro seja encontrado encerra o loop
                break

            try:
                if  '.' not in self.world_knowledge[self.world.agent_row-1][self.world.agent_col] and self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('u'):       # Movimento do agente para cima
                            already_moved = True # inicia movimento do agente

            except IndexError:
                pass

            try:
                if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col+1] and self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                    if already_moved == False:
                        if self.move('r'):       # Movimento do agente para direita
                            already_moved = True # inicia movimento do agente
            except IndexError:
                pass

            try:
                if '.' not in self.world_knowledge[self.world.agent_row+1][self.world.agent_col] and self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('d'):       # Movimento do agente para baixo
                            already_moved = True # inicia movimento do agente
            except IndexError:
                pass

            try:
                if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col-1] and self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                    if already_moved == False:
                        if self.move('l'):       # Movimento do agente para esquerda
                            already_moved = True # inicia movimento do agente
            except IndexError:
                pass


            if already_moved == False:  # se o agente  nao estiver se movendo 
                self.go_back_one_tile() # volta um quadrado caso nao seja seguro

            already_moved = False
          


    def move(self, direction): # Funcao com definicoes de direcoes de Movimento do agente

        self.repaint_world()

        if self.found_gold == True and self.took_gold == False: # se o ouro foi encontrado e nao foi levado
            self.took_gold == True # pega o ouro 
            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('G') # remove o simbolo G quando o ouro e pego

        successful_move = False
        if direction == 'u':
            if self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                successful_move = self.move_up() # Inicia movimento para cima 
        if direction == 'r':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                successful_move = self.move_right()  # Inicia movimento para direita 
        if direction == 'd':
            if self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                successful_move = self.move_down() # Inicia movimento para baixo
        if direction == 'l':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                successful_move = self.move_left() # Inicia movimento para esquerda

        if successful_move: # Apos a realizacao do movimento
            self.add_indicators_to_knowledge() # atualiza indicadores de dados(conhecimentos) obtidos
            self.mark_tile_visited() # atualiza a celula ja visitada
        
            self.predict_pits()      # atualiza predicoes d localizacao de pocos
            self.clean_predictions()

    
            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                
                self.found_gold = True # se o ouro foi encontrado nao precisa retornar para fora da caverna

            if self.found_gold == False: # se o ouro não foi encontrado
                self.path_out_of_cave.append([self.world.agent_row, self.world.agent_col])


            time.sleep(1.5)    # Tempo de atualizacao de acoes
        return successful_move # retorna movimento a ser realizado


    def add_indicators_to_knowledge(self): # Funcao que adiciona indicadores de base de conhecimento KB
    
        #Indicadores de dados(conhecimento) adquiridos em relação a localização de Brisas
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'B' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('B')
                
                
         #Indicadores de dados(conhecimento) adquiridos em relação a localização do ouro
        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'G' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('G')
                
        #Indicadores de dados(conhecimento) adquiridos em relação a localização dos poços
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'P' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('P')
                

    def predict_pits(self): # funcao que realiza a previsao onde os poços se encontram a parti dos dados(conhecimentos) ja adiquiridos ate aquele momento
        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'p' not in self.world_knowledge[self.world.agent_row-1][self.world.agent_col]:
                            self.world_knowledge[self.world.agent_row-1][self.world.agent_col].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.num_cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'p' not in self.world_knowledge[self.world.agent_row][self.world.agent_col+1]:
                            self.world_knowledge[self.world.agent_row][self.world.agent_col+1].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.num_rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'p' not in self.world_knowledge[self.world.agent_row+1][self.world.agent_col]:
                            self.world_knowledge[self.world.agent_row+1][self.world.agent_col].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'p' not in self.world_knowledge[self.world.agent_row][self.world.agent_col-1]:
                            self.world_knowledge[self.world.agent_row][self.world.agent_col-1].append('p')
        except IndexError:
            pass


    def clean_predictions(self): # Limpa as previsoes apos ter certeza onde se encontra elementos da caverna
        self.num_stenches = 0

        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                
                if 'p' in self.world_knowledge[i][j]: # utiliza conhecimentos obtidos em relacao a posicao dos pocos 
                    try:
                        if i-1 >= 0:
                            if '.' in self.world_knowledge[i-1][j]:
                                if 'B' not in self.world_knowledge[i-1][j]: # utiliza conhecimentos obtidos em relacao a posicao das brisas
                                    self.world_knowledge[i][j].remove('p')
                                    self.world_knowledge[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols: # se for menor que o numero de colunas
                            if '.' in self.world_knowledge[i][j+1]:
                                if 'B' not in self.world_knowledge[i][j+1]:
                                    self.world_knowledge[i][j].remove('p') # remove a informacao da posicao do poco no mapa caso nao tenha poco
                                    self.world_knowledge[i][j].append('np') # remove a informacao quando se verifica que nao ha poco na pasicao 
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows: # se for menor que o numero de linhas
                            if '.' in self.world_knowledge[i+1][j]:
                                if 'B' not in self.world_knowledge[i+1][j]:
                                    self.world_knowledge[i][j].remove('p') # remove a informacao da posicao do poco no mapa caso nao tenha poco
                                    self.world_knowledge[i][j].append('np') # remove a informacao quando se verifica que nao há poço na pasicao
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0: # se a posição da coluna -1 for maior ou igua a zero
                            if '.' in self.world_knowledge[i][j-1]: # utiliza o conhecimento adiquirido ate o momento
                                if 'B' not in self.world_knowledge[i][j-1]:
                                    self.world_knowledge[i][j].remove('p')  # remove a informação da posicao do poço no mapa caso não tenha poco
                                    self.world_knowledge[i][j].append('np') # remove a informacao quando se verifica que nao ha poco na pasicao
                    except IndexError:
                        pass


    def move_up(self): # funcao que realiza o movimento para cima do agente
        try:
            if self.world.agent_row-1 >= 0:
                self.remove_agent()
                self.world.agent_row -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_right(self): # funcao que realiza o movimento para a direita do agente
        try:
            if self.world.agent_col+1 < self.world.num_cols:
                self.remove_agent()
                self.world.agent_col += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_down(self): # funcao que realiza o movimento para baixo do agente
        try:
            if self.world.agent_row+1 < self.world.num_rows:
                self.remove_agent()
                self.world.agent_row += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_left(self): # funcao que realiza o movimento para esquerda do agente
        try:
            if self.world.agent_col-1 >= 0:
                self.remove_agent()
                self.world.agent_col -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def remove_agent(self): # Funcao que realiza a remocao do agente 
        self.world.world[self.world.agent_row][self.world.agent_col].remove('A')
        self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('A')


    def add_agent(self): # funcao que realiza o adicionamento de agente no mundo
        self.world.world[self.world.agent_row][self.world.agent_col].append('A')
        self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')


    def mark_tile_visited(self): # funcao que marca quadrados ja visitados
        if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append('.')
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('.')


    def is_dead(self): # Função que indica se o agente morreu (caiu em um poço ) Nao temos Wumpus
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]: 
            print("You have fallen in a pit!")
            return True # caso o agente cai em um poço ele morre (perde)
        else:
            return False


    def is_safe_move(self, row, col): # Funcao que verifica se e seguro se mover para um certo quadrado
        try:
            if 'p' in self.world_knowledge[row][col]: # utiliza de dados (conhecimentos) ja adiquiridos ate o momento para verificar se o caminho e seguro em relacao aos pocos
                return False
        except IndexError:
            pass
      
        try:
            if 'P' in self.world_knowledge[row][col]: # utiliza de dados (conhecimentos) ja adiquiridos ate o momento para verificar se o caminho e seguro em relacao aos pocos
                return False
        except IndexError:
            pass

        return True

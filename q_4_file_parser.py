# Prova 3 -IA - Questao 4
# Aluno: Breno Linhares de Sousa- 170007057
# Codigo modificado de : https://github.com/alexander-bachmann/wumpus-world

#Arquivo: file parser.py: Puxa do arquivo os dados do posicionamento(cordenadas) dos elemenstos do mundo de wumpus

"""
4 5     # number of rows and cols
A 4 0   # agent starting coordinates
W 1 0   # wumpus coordinates
G 1 1   # gold coordinates
P 0 3   # 1st pit coordinates
P 1 2   # 2nd pit coordinates
P 3 2   # 3rd pit coordinates
"""

# coordenadas (posicoes) elemento do mundo de wumpus
class File_Parser:
    def __init__(self, world_file):
        self.row_col = []
        self.agent = []
        self.gold = []
        self.pits = [[]]

        file = open(world_file, 'r')

        self.row_col = file.readline()
        self.row_col = self.row_col.rstrip('\r\n')
        self.row_col = self.row_col.split(" ")

        self.agent = file.readline()
        self.agent = self.agent.rstrip('\r\n')
        self.agent = self.agent.split(" ")


        self.gold = file.readline()
        self.gold = self.gold.rstrip('\r\n')
        self.gold = self.gold.split(" ")

        self.pits = []

        while True:
            pit = file.readline()
            if len(pit) == 0:
                break
            pit = pit.rstrip('\r\n')
            pit = pit.split(" ")

            self.pits.append(pit)

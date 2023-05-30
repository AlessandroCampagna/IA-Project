# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 24:
# 106751 Alessandro Campagna
# 00000 Nome2

import sys
import numpy as np
from sys import stdin,stdout

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id



class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows, columns, hints, ships, board):
        
        self.rows = rows
        self.columns = columns
        self.hints = hints
        self.ships = ships
        self.board = board
        
        for hint in hints:
            self.board[hint[0]][hint[1]] = hint[2]
            
            if hint[2] != "W":
                self.rows[hint[0]]-=1
                self.columns[hint[1]]-=1
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        
        if col == 9:
            return (self.board[row][col-1],None)
        else:
            return (self.board[row][col-1],self.board[row][col+1])

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        
        if row == 9:
            return (self.board[row-1][col],None)
        else:
            return (self.board[row-1][col],self.board[row+1][col])

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # Read the input
        lines = stdin.readlines()

        # Get the row and column values
        rows = np.array([int(x) for x in lines[0].split()[1:]])
        columns = np.array([int(x) for x in lines[1].split()[1:]])
        
        # Get the number of hints
        hintNum = int(lines[2])

        # Get the Hints
        hints = np.zeros(hintNum, dtype=object)
        for i in range(hintNum):
            hintLine = lines[3+i].split()
            hints[i] = ((int(hintLine[1]), int(hintLine[2]), hintLine[3]))

        return Board(rows,columns,hints,[4,3,3,2,2,2,1,1,1,1],np.full((10,10),None))
    
    def output(self):
        
        for r in range(10):
            stdout.write("\n")
            for c in range(10):
                if self.board[r][c]=="w" or self.board[r][c]==None:
                    stdout.write(".")
                else:
                    stdout.write(self.board[r][c])

        print()
    
    def print(self):

        print(" ", end=" ")
        for c in range(10):
            print(self.columns[c], end=" ")
        print()
        for r in range(10):
            print(self.rows[r], end=" ")
            for col in range(10):
                if self.board[r][col] == None:
                    print(".", end=" ")
                else:
                    print(self.board[r][col], end=" ")
            print()
        print()
    
    def canPlace(self, row, col, ship, orientation=None):
        
        if orientation == None:
            if (
                
                ship != 1 or
                
                ship not in self.ships or
                
                (self.board[row][col] != None and self.board[row][col] != "C") or
                row < 0 or row > 9 or
                col < 0 or col > 9 or
                self.rows[row] <= 0 or self.columns[col] <= 0 or
                
                any(
                    (self.board[y][x] != None and self.board[y][x] != "w")
                    for y in range(row-1, row+2) 
                    for x in range(col-1, col+2) 
                    if (y, x) != (row, col) and x >= 0 and x <= 9 and y >= 0 and y <= 9
                    )
                
                ):
                
                return False
        
        elif orientation == "H":
            if ( 
                
                ship not in self.ships or
                
                row > 9 or row < 0 or
                col+ship > 9 or col < 0 or
                
                (self.board[row][col+ship] != None and
                self.board[row][col+ship] != "w") or
                
                (self.board[row][col-1] != None and
                self.board[row][col-1] != "w") or
                
                (self.adjacent_vertical_values(row,col+ship) != ("w","w") and
                self.adjacent_vertical_values(row,col+ship) != (None,"w") and
                self.adjacent_vertical_values(row,col+ship) != ("w",None) and
                self.adjacent_vertical_values(row,col+ship) != (None,None)) or
                
                (self.adjacent_vertical_values(row,col-1) != ("w","w") and
                self.adjacent_vertical_values(row,col-1) != (None,"w") and
                self.adjacent_vertical_values(row,col-1) != ("w",None) and
                self.adjacent_vertical_values(row,col-1) != (None,None)) or
                
                (self.board[row][col] != None and self.board[row][col] != "T") or
                
                self.rows[row] <= 0 or self.columns[col] <= 0 or
                
                (self.board[row][col+ship-1] != None and self.board[row][col+ship-1] != "B") or
                
                self.rows[row] <= 0 or self.columns[col+ship-1] <= 0 or
                
                any(((self.board[row][col+i] != None and self.board[row][col+i] != "M") or self.rows[row]<=0 or self.columns[col+1]<=0) for i in range(1,ship-1))
                
                ):
                
                return False
        
        elif orientation == "V":
            if ( 
                
                ship not in self.ships or
                
                row+ship > 9 or row < 0 or
                
                col > 9 or col < 0 or
                
                (self.board[row+ship][col] != None and
                self.board[row+ship][col] != "w") or
                
                (self.board[row-1][col] != None and
                self.board[row-1][col] != "w") or
                
                (self.adjacent_horizontal_values(row+ship,col) != ("w","w") and
                self.adjacent_horizontal_values(row+ship,col) != (None,"w") and
                self.adjacent_horizontal_values(row+ship,col) != ("w",None) and
                self.adjacent_horizontal_values(row+ship,col) != (None,None)) or
                
                (self.adjacent_horizontal_values(row-1,col) != ("w","w") and
                self.adjacent_horizontal_values(row-1,col) != (None,"w") and
                self.adjacent_horizontal_values(row-1,col) != ("w",None) and
                self.adjacent_horizontal_values(row-1,col) != (None,None)) or
                
                (self.board[row][col] != None and self.board[row][col] != "L") or
                
                self.rows[row] <= 0 or self.columns[col] <= 0 or
                
                (self.board[row+ship-1][col] != None and self.board[row+ship-1][col] != "R") or
                
                self.rows[row+ship-1] <= 0 or self.columns[col] <= 0 or
                
                any(((self.board[row+i][col] != None and self.board[row+i][col] != "M") or self.rows[row+i]<=0 or self.columns[col <= 0]) for i in range(1,ship-1))
                
                ):
                
                return False
            
        return True
    
    def copy(self):
        return Board(self.rows,self.columns,self.hints,self.ships.copy(),self.board)

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board=state.board

        actionsList = []
        
        for row in range(10):
            for col in range(10):
                for ship in board.ships:
                    if board.board[row][col] == None:
                        if ship == 1:
                            if board.canPlace(row,col,ship):
                                actionsList.append((row,col,ship,None))
                        else :
                            if board.canPlace(row,col,ship,"H"):
                                actionsList.append((row,col,ship,"H"))
                            if board.canPlace(row,col,ship,"V"):
                                actionsList.append((row,col,ship,"V"))
                if board.board[row][col] == "T" and ship > 1:
                    if board.canPlace(row,col,ship,"V"):
                        actionsList.append((row,col,ship,"V"))
                
                if board.board[row][col] == "L" and ship > 1:
                    if board.canPlace(row,col,ship,"H"):
                        actionsList.append((row,col,ship,"H"))
                    
                
                    
        return actionsList

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        
        board = state.board.copy()
        
        if action[3] == None:
            
            for y in range(3):
                for x in range(3):
                    if 0 <= y+action[0]-1 < 10 and 0 <= x+action[1]-1 < 10 and (board.board[action[0]+y-1][action[1]+x-1] == None or board.board[action[0]+y-1][action[1]+x-1] == "w"):
                        board.board[action[0]+y-1][action[1]+x-1] = "w"
                        
            if board.board[action[0]][action[1]] != "C":
                board.board[action[0]][action[1]] = "c"
                board.rows[action[0]] -=1
                board.columns[action[1]] -=1
                if board.rows[action[0]]==0:
                    board.board[action[0]] = np.full(10, "w")
                if board.columns[action[1]]==0:
                     board.board[:,action[1]] = np.full(10, "w")               
            
            board.ships.remove(1)
        
        elif action[3] == "H":
            
            for y in range(3):
                for x in range(action[2]):
                    
                    if 0 <= y+action[0]-1 < 10 and 0 <= x+action[1]-1 < 10 and (board.board[action[0]+y-1][action[1]+x-1] == None or board.board[action[0]+y-1][action[1]+x-1] == "w"):
                        if y == 1 and x == 1:
                            board.board[action[0]+y-1][action[1]+x-1] = "l"
                            board.rows[action[0]+y-1] -=1
                            board.columns[action[1]+x-1] -=1
                            
                        elif y == 1 and x == action[2]:
                            board.board[action[0]+y-1][action[1]+x-1] = "r"
                            board.rows[action[0]+y-1] -=1
                            board.columns[action[1]+x-1] -=1
                            
                        elif y == 1 and 1 < x < action[2]:
                            board.board[action[0]+y-1][action[1]+x-1] = "m"
                            board.rows[action[0]+y-1] -=1
                            board.columns[action[1]+x-1] -=1
                            
                        else:
                            board.board[action[0]+y-1][action[1]+x-1] = "w"
                            
                        if board.rows[action[0]+y-1]==0:
                            board.board[action[0]+y-1] = np.full(10, "w")
                            
                        if board.columns[action[1]+x-1]==0:
                            board.board[:,action[1]+x-1] = np.full(10, "w")
                            
            board.ships.remove(action[2])

        elif action[3] == "V":
            
            for y in range(action[2]):
                for x in range(3):
                    
                    if 0 <= y+action[0]-1 < 10 and 0 <= x+action[1]-1 < 10 and (board.board[action[0]+y-1][action[1]+x-1] == None or board.board[action[0]+y-1][action[1]+x-1] == "w"):
                        if y == 1 and x == 1:
                            board.board[action[0]+y-1][action[1]+x-1] = "t"
                            board.rows[action[0]+y-1] -=1
                            board.columns[action[1]+x-1] -=1
                            
                        elif y == action[2] and x == 1:
                            board.board[action[0]+y-1][action[1]+x-1] = "b"
                            board.rows[action[0]+y-1] -=1
                            board.columns[action[1]+x-1] -=1
                            
                        elif x == 1 and 1 < y < action[2]:
                            board.board[action[0]+y-1][action[1]+x-1] = "m"
                            board.rows[action[0]+y-1] -=1
                            board.columns[action[1]+x-1] -=1
                            
                        else:
                            board.board[action[0]+y-1][action[1]+x-1] = "w"     
                        
                        if board.rows[action[0]+y-1]==0:
                            board.board[action[0]+y-1] = np.full(10, "w")
                            
                        if board.columns[action[1]+x-1]==0:
                            board.board[:,action[1]+x-1] = np.full(10, "w")  
            
            board.ships.remove(action[2])
            
            board.print()
            print(action)
            print(board.ships)
            
        return BimaruState(board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        # Get the current game board
        board = state.board
        
        # Check if all the ships are placed
        if len(board.ships) != 0:
            return False
        
        # Check if all the ships are placed correctly
        for row in range(10):
            for col in range(10):
                if board.board[row][col] == None:
                    return False

        return True
                    

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        
        pass



if __name__ == "__main__":
    
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    depth_first_tree_search(bimaru).state.board.output()
    

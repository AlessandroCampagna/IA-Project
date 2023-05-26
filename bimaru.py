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

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows, columns, hints):
        
        self.board = np.full((10,10), None)
        self.rows = rows
        self.columns = columns
        self.hints = hints
        self.ships = [4,3,3,2,2,2,1,1,1,1]
        
        for hint in hints:
            self.board[hint[0]][hint[1]] = hint[2]
            
            if hint[2] != "W":
                self.rows[hint[0]]-=1
                self.columns[hint[1]]-=1
                
        for r,row in enumerate(self.rows):
            if row == 0:
                self.board[r] = np.full(10, "w")
                
        for c,col in enumerate(self.columns):
            if col == 0:
                self.board[:,c] = np.full(10, "w")
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.board[row][col-1],self.board[row][col+1])

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
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

        return Board(rows,columns,hints)
    
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
                
                any(
                    (self.board[y][x] != None and self.board[y][x] != "w") 
                    for y in range(row-1, row+2) 
                    for x in range(col-1, col+2) 
                    if (y, x) != (row, col)
                    )
                
                ):
                
                return False
        
        elif orientation == "H":
            if ( 
                
                ship not in self.ships or
                
                row > 9 or row < 0 or
                col+ship-1 > 9 or col < 0 or
                
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
                
                (self.board[row][col+ship-1] != None and self.board[row][col+ship-1] != "B") or
                
                any((self.board[row][col+i] != None and self.board[row][col+i] != "M") for i in range(1,ship-1))
                
                ):
                
                return False
        
        elif orientation == "V":
            if ( 
                
                ship not in self.ships or
                
                row+ship-1 > 9 or row < 0 or
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
                
                (self.board[row+ship-1][col] != None and self.board[row+ship-1][col] != "R") or
                
                any((self.board[row+i][col] != None and self.board[row+i][col] != "M") for i in range(1,ship-1))
                
                ):
                
                return False
            
        return True

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
        
        for ri,r in enumerate(board.rows):
            for ci,c in enumerate(board.columns):
                
                value = board.get_value(ri,ci)
                
                
                    
        return actionsList

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        # Get the current game board
        board = state.board
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    
    board = Board.parse_instance()
    board.print()
    print(board.adjacent_vertical_values(0,0))
            
    


# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
import numpy as np
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
    
    def __init__(self, rows, columns, ships, board):
        
        self._rows = rows
        self._columns = columns
        self._ships = ships
        self._board = board
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.inBounds(row, col):
            return self._board[row][col]
        else:
            return None

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if self.inBounds(row-1, col) and self.inBounds(row+1, col):
            return self._board[row-1][col], self._board[row+1][col]
        elif self.inBounds(row-1, col):
            return self._board[row-1][col], None
        elif self.inBounds(row+1, col):
            return None, self._board[row+1][col]
        else:
            return None, None

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if self.inBounds(row, col-1) and self.inBounds(row, col+1):
            return self._board[row][col-1], self._board[row][col+1]
        elif self.inBounds(row, col-1):
            return self._board[row][col-1], None
        elif self.inBounds(row, col+1):
            return None, self._board[row][col+1]
        else:
            return None, None

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        """
        from sys import stdin
        
        board = np.full((10,10),None)
        
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
            
        for hint in hints:
            board[hint[0]][hint[1]] = hint[2]
            if hint[2] != "W":
                rows[hint[0]]-=1
                columns[hint[1]]-=1

        return Board(rows,columns,[4,3,3,2,2,2,1,1,1,1],board)
    
    def output(self):
        for r in range(10):
            for c in range(10):
                if self._board[r][c] == "w" or self._board[r][c] is None:
                    print(".", end="")
                else:
                    print(self._board[r][c], end="")
            print()

    def inBounds (self, row, col):
        return row >= 0 and row < 10 and col >= 0 and col < 10
    
    def numHintsShipPlacement(self, row, col, ship, orientation):
        count = 0
        for i in range(ship):
            if orientation == "H":
                value = self.get_value(row, col+i)
                if value in ["L","R","M"]:
                    count+=1
            elif orientation == "V":
                value = self.get_value(row+i, col)
                if value in ["T","B","M"]:
                    count+=1
        return count
    
    def freeCell(self, row, col):
        
        return self.inBounds(row, col) and self.get_value(row, col) == None and self._rows[row] > 0 and self._columns[col] > 0
    
    def freeShipPlacement(self, row, col, ship, orientation):
        
        if orientation == None:
            return self.freeCell(row, col) or self.get_value(row, col) == "C"
        
        elif orientation == "H":
            return (self._rows[row] >= ship - self.numHintsShipPlacement(row,col,ship,orientation) and 
                    (self.freeCell(row, col) or self.get_value(row, col) == "L") and
                    (self.freeCell(row, col+ship-1) or self.get_value(row, col+ship-1) == "R") and
                    all(self.freeCell(row, c) or self.get_value(row, c) == "M" for c in range(col+1, col+ship-1)))
        
        elif orientation == "V":
            return (self._columns[col] >= ship - self.numHintsShipPlacement(row,col,ship,orientation) and
                    (self.freeCell(row, col) or self.get_value(row, col) == "T") and
                    (self.freeCell(row+ship-1, col) or self.get_value(row+ship-1, col) == "B") and
                    all(self.freeCell(r, col) or self.get_value(r, col) == "M" for r in range(row+1, row+ship-1)))
    
    def validSurrounding(self, row, col, ship, orientation):
        
        if orientation == None:
            return all(self.get_value(r,c)==None or self.get_value(r,c)=="w" or self.get_value(r,c)=="W" for r in range(row-1, row+2) for c in range(col-1, col+2) if (r,c)!=(row,col))
        
        elif orientation == "H":
            return all(self.get_value(r,c)==None or self.get_value(r,c)=="w" or self.get_value(r,c)=="W" for r in range(row-1, row+2) for c in range(col-1, col+ship+1) if not (r==row and c >= col and c < col+ship))
        
        elif orientation == "V":
            return all(self.get_value(r,c)==None or self.get_value(r,c)=="w" or self.get_value(r,c)=="W" for r in range(row-1, row+ship+1) for c in range(col-1, col+2) if not (c==col and r >= row and r < row+ship))
        
    
    def canPlaceShip(self, row, col, ship, orientation):
        return self.validSurrounding(row, col, ship, orientation) and self.freeShipPlacement(row, col, ship, orientation)
    
    def fillRow(self,row):
        for c in range(10):
            if self.get_value(row, c) == None:
                self._board[row][c] = "w"
                
    def fillColumn(self,col):
        for r in range(10):
            if self.get_value(r, col) == None:
                self._board[r][col] = "w"

    def placeCell(self, row, col, cell):
        self._board[row][col] = cell
        self._rows[row] -= 1
        self._columns[col] -= 1
        if self._rows[row] <= 0:
            self.fillRow(row)
        if self._columns[col] <= 0:
            self.fillColumn(col)

    def placeShip(self, row, col, ship, orientation):
        
        if orientation == None:
            if self.freeCell(row, col):
                self.placeCell(row, col, "c")
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if self.inBounds(r, c) and self.get_value(r, c) == None:
                        self._board[r][c] = "w"
    
        elif orientation == "H":
            for r in range (row-1, row+2):
                for c in range(col-1, col+ship+1):
                    if self.inBounds(r, c) and self.get_value(r, c) == None:
                        if not (r==row and c >= col and c < col+ship):
                            self._board[r][c] = "w"
                        elif c == col and self._board[r][c] == None:
                            self.placeCell(r,c,"l")
                        elif c == col+ship-1 and self._board[r][c] == None:
                            self.placeCell(r,c,"r")
                        elif self._board[r][c] == None:
                            self.placeCell(r,c,"m")
                            
        elif orientation == "V":
            for r in range (row-1, row+ship+1):
                for c in range(col-1, col+2):
                    if self.inBounds(r, c) and self.get_value(r, c) == None:
                        if not (c==col and r >= row and r < row+ship):
                            self._board[r][c] = "w"
                        elif r == row and self._board[r][c] == None:
                            self.placeCell(r,c,"t")
                        elif r == row+ship-1 and self._board[r][c] == None:
                            self.placeCell(r,c,"b")
                        elif self._board[r][c] == None:
                            self.placeCell(r,c,"m")
        
        self._ships.remove(ship)
        if self._ships == []:
            for r in range(10):
                self.fillRow(r)

    def copy(self):
        rows_copy = self._rows.copy()
        columns_copy = self._columns.copy()
        ships_copy = self._ships.copy()
        board_copy = self._board.copy()

        return Board(rows_copy, columns_copy, ships_copy, board_copy)

    def isGoal(self):
        return self._ships == [] 
    
    def print(self):

        print(" ", end=" ")
        for c in range(10):
            print(self._columns[c], end=" ")
        print()
        for r in range(10):
            print(self._rows[r], end=" ")
            for col in range(10):
                if self._board[r][col] == None:
                    print(".", end=" ")
                else:
                    print(self._board[r][col], end=" ")
            print()
        print()


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        for r in range(10):
            if board._rows[r] == 0:
                board.fillRow(r)
        for c in range(10):
            if board._columns[c] == 0:
                board.fillColumn(c)
        
        super().__init__(BimaruState(board))

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actionsList = []
        
        for row in range(10):
            for col in range(10):
                value = state.board.get_value(row, col)
                if value == "C":
                    if 1 in state.board._ships:
                        actionsList.append((row,col,1,None))
                elif value == "L":
                    for ship in range(2,5):
                        if ship in state.board._ships and state.board.canPlaceShip(row,col,ship,"H"):
                            actionsList.append((row,col,ship,"H"))
                elif value == "R":
                    for ship in range(2,5):
                        if ship in state.board._ships and state.board.canPlaceShip(row,col-ship+1,ship,"H"):
                            actionsList.append((row,col-ship+1,ship,"H"))
                elif value == "T":
                    for ship in range(2,5):
                        if ship in state.board._ships and state.board.canPlaceShip(row,col,ship,"V"):
                            actionsList.append((row,col,ship,"V"))
                elif value == "B":
                    for ship in range(2,5):
                        if ship in state.board._ships and state.board.canPlaceShip(row-ship+1,col,ship,"V"):
                            actionsList.append((row-ship+1,col,ship,"V"))
                elif value == "M":
                    for ship in range(2,5):
                        if ship in state.board._ships and state.board.canPlaceShip(row,col-1,ship,"H"):
                            actionsList.append((row,col-1,ship,"H"))
                        if ship in state.board._ships and state.board.canPlaceShip(row-1,col,ship,"V"):
                            actionsList.append((row-1,col,ship,"V"))
                    if 4 in state.board._ships and state.board.canPlaceShip(row,col-2,4,"H"):
                        actionsList.append((row,col-2,4,"H"))
                    if 4 in state.board._ships and state.board.canPlaceShip(row-2,col,4,"V"):
                        actionsList.append((row-2,col,4,"V"))
        
        for row in range(10):
            for col in range(10):
                for ship in state.board._ships:
                    if ship == 1:
                        if state.board.canPlaceShip(row,col,ship,None):
                            actionsList.append((row,col,ship,None))
                    else :
                        if state.board.canPlaceShip(row,col,ship,"H"):
                            actionsList.append((row,col,ship,"H"))
                        if state.board.canPlaceShip(row,col,ship,"V"):
                            actionsList.append((row,col,ship,"V"))
        
        return actionsList

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        board = state.board.copy()
        board.placeShip(action[0], action[1], action[2], action[3])
        print(action)
        print(board._ships)
        board.print()
    
        return BimaruState(board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        return state.board.isGoal()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":

    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    board = Board.parse_instance()
    board.print()
    bimaru = Bimaru(board)
    board.print()
    
    
    goal = depth_first_tree_search(bimaru)
    print(goal.state.board.output())
    
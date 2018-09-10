import math
import itertools

# Matrix class
class Matrix(object):
    def __init__(self,linhas = list()):
        self.linhas = linhas
        if type(linhas) == list:
            if len(set([len(i) for i in linhas])) > 1:
                print("Error: matrix not created, size of rows is inconsistent.")
            else:
                if len(linhas) == 0:
                    self.shape = (0,0)
                else:
                    self.shape = (len(linhas),len(linhas[0]))
        else:
            print("Error: Data structure must contain a list of lists (eg: [[1,2],[3,4]]).")
    
    def __str__(self):
        s = '\n'
        for linha in self.linhas:
            ss = ''
            for coluna in linha:
                ss = ss + ' %7.2f ' % coluna
            s =  s + '|' + ss + '|\n'
        return s
    
    def __getitem__(self, item):
        i,j = item
        if type(j) is slice or type(i) is slice:
            subset = self.linhas[i]
            if type(subset[0]) is not list:
                subset = [subset]
            yisslice = type(j) is slice
            for cj in range(len(subset)):
                subset[cj] = subset[cj][j]
                if not yisslice:
                    subset[cj] = [subset[cj]]
            return Matrix(subset)
        else:
            return self.linhas[i][j]
    
                
    def __setitem__(self, item, value):
        i, j = item
        if type(i) is slice or type(j) is slice:
            for n in [i,j]:
                n_ = n
                n = slice(n, n+1) if type(n) != slice else n
                n = slice(0, -1) if type(n) == None else n
                n = slice(0, n.stop) if n.start == None else n
                n = slice(n.start, self.shape[0 if n_ == i else 1]) if n.stop == None else n
                i = n if n_ == i else i
                j = n if n_ == j else j
            
            if type(value) in [float,int]:
                value = Matrix([[value]*self.shape[1]]*self.shape[0])
            elif value.shape[0] != i.stop - i.start or value.shape[1] != j.stop - j.start:
                print("Error: incompatible dimensions.")
                return False
            elif value.shape[0] == self.shape[0] or value.shape[1] == self.shape[1]:
                if value.shape[0] == 1:
                    value = Matrix([value.linhas[0]] * self.shape[1])
                elif value.shape[1] == 1:
                    value = Matrix([n*self.shape[0] for n in value.linhas])
            for linha in range(i.start, i.stop) if self.shape[0] != 1 else [0]:
                for coluna in range(j.start, j.stop) if self.shape[1] != 1 else [0]:
                    self[linha,coluna] = value[linha,coluna]
        else:
            self.linhas[i][j] = value


    def __add__(self, value):
        if type(value) == Matrix:
            if self.shape != value.shape:
                print("Error: incompatible dimensions.")
                return False
            else:
                result = self
                
                for (i,j) in itertools.product(range(self.shape[0]),range(self.shape[1])):
                    result[i,j] = result[i,j] + value[i,j]
        elif type(value) in [int,float]:
            result = self + Matrix([[value]*self.shape[1]]*self.shape[0])
        return result
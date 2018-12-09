import math
from random import random

# ones method
def ones(dimensions):
    return (rand(dimensions) * 0) + 1

# zeros method
def zeros(dimensions):
    return rand(dimensions) * 0

# rand method
def rand(dimensions):
    if type(dimensions) not in [int, tuple]:
        print("Error: inconsistent dimensions.")
        return False
    if type(dimensions) == int:
        dimensions = (dimensions, dimensions)
    return Matrix([[random() for i in range(dimensions[1])] for j in range(dimensions[0])])

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
        if type(i) is int and type(j) is int:
            return self.linhas[i][j]

        list_index = [0,0]
        for dim,count in [(i,0),(j,1)]:
            if type(dim) is int:
                list_index[count] = [self.shape[count] + dim if dim < 0 else dim]

            if type(dim) is slice:
                start = 0 if dim.start == None else dim.start
                step  = 1 if dim.step == None else dim.step
                stop = self.shape[count] if dim.stop == None else dim.stop
                step = -1 if start > stop and step == 1 else step

                if stop > start and step < 0:
                    stop, start = start, stop-1

                list_index[count] = list(range(start, stop,step))

            if type(dim) is list:
                list_index[count] = dim

        result = list()
        for row in list_index[0]:
            aux_list = list()
            for col in list_index[1]:
                aux_list.append(self.linhas[row][col])
            result.append(aux_list)

        return Matrix(result)
                # slice(dim.start, dim.step, dim.stop)
                # list_index.append(range(self.shape[dimension]+1) if dimension == None else 1)
                # print(list_index[dimension])





        # if type(i) is slice or type(j) is slice:
        #     for n in [i,j]:
        #         n_ = n
        #         n = slice(n, n+1) if type(n) != slice else n
        #         n = slice(0, -1) if type(n) == None else n
        #         n = slice(0, n.stop) if n.start == None else n
        #         n = slice(n.start, self.shape[0 if n_ == i else 1]) if n.stop == None else n
        #         i = n if n_ == i else i
        #         j = n if n_ == j else j

        #     result = zeros((i.stop-i.start, j.stop-j.start))
        #     for linha in range(i.start, i.stop) if self.shape[0] != 1 else [0]:
        #         for coluna in range(j.start, j.stop) if self.shape[1] != 1 else [0]:
        #             # print(linha,coluna)
        #             result[linha-i.start,coluna-j.start] = self.linhas[linha][coluna]
        #     return result
        # else:
        #     return self.linhas[i][j]
    
                
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
                    self[linha,coluna] = value[linha-i.start,coluna-j.start]

        else:
            self.linhas[i][j] = value


    def __add__(self, value):
        if type(value) == Matrix:
            if self.shape != value.shape:
                print("Error: incompatible dimensions.")
                return False
            else:
                result = self
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        result[i,j] = result[i,j] + value[i,j]
        elif type(value) in [int,float]:
            result = self + Matrix([[value]*self.shape[1]]*self.shape[0])
        return result

    def __sub__(self, value):
        if type(value) == Matrix:
            if self.shape != value.shape:
                print("Error: incompatible dimensions.")
                return False
            else:
                result = self
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        result[i,j] = result[i,j] - value[i,j]
        elif type(value) in [int,float]:
            result = self - Matrix([[value]*self.shape[1]]*self.shape[0])
        return result

    def __mul__(self, value):
        result = self
        if type(value) in [int, float]:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    result[i,j] = result[i,j] * value
        elif type(value) == Matrix and self.shape[1] != value.shape[0]:
            print("Error: Matrices with Incompatible Dimensions.")
            result = None
        else:
            result = zeros((self.shape[0], value.shape[1]))
            if self.shape[0] == 1 and value.shape[1] == 1:
                result = 0
                for i in range(self.shape[1]):
                    result = result + self[0,i] * value[i,0]
            else:
                result = zeros((self.shape[0], value.shape[1]))
                for i in range(self.shape[0]):
                    for j in range(value.shape[1]):
                        result[i,j] = self[i,:] * value[:,j]
        return result

    def __abs__(self):
        return self.dot_operation(abs)

    def transpose(self):
        result = zeros((self.shape[1], self.shape[0]))
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[j,i] = self[i,j]
        return result

    def sum(self, axis=0):
        if 1 in self.shape:
            result = 0
            if self.shape[0] == 1:
                for i in range(self.shape[1]):
                    result = result + self[0,i]
            else:
                for i in range(self.shape[0]):
                    result = result + self[i,0]
        else:
            if axis == 0:
                result = zeros((1,self.shape[1]))
                for i in range(self.shape[1]):
                    result[0,i] = self[:,i].sum()
            else:
                result = zeros((self.shape[0],1))
                for i in range(self.shape[0]):
                    result[i,0] = self[i,:].sum()
        return result

    # def min_max(self, axis=0, op='max', arg=False):
    #     if 1 in self.shape:
    #         result = 0
    #         if self.shape[0] == 1:
    #             linhas = self.linhas[0]
    #             if op == 'max':
    #                 op_value = max(linhas)
    #             elif op == 'min':
    #                 op_value = min(linhas)
    #             result = op_value if not arg else linhas.index(op_value)
    #         else:
    #             result = self.transpose().min_max(axis=axis, op=op, arg=arg)
    #     else:
    #         aux = self
    #         result = zeros((1,self.shape[1]))
    #         aux = self.transpose() if axis == 0 else aux
    #         for i in range(self.shape[1]):
    #             result[0,i] = aux[:,i].min_max(axis=axis, op=op, arg=arg)
    #         result = result.transpose() if axis == 0 else result
    #     return result

    # def min(self, axis=0):
    #     return self.min_max(axis=axis, op='min')
    # def argmin(self, axis=0):
    #     return self.min_max(axis=axis, op='min', arg=True)

    # def max(self, axis=0):
    #     return self.min_max(axis=axis, op='max')
    # def argmax(self, axis=0):
    #     return self.min_max(axis=axis, op='max', arg=True)

    def dot(self, value):
        result = zeros(self.shape)
        if type(value) == Matrix and self.shape == value.shape:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    result[i,j] = self[i,j] * value[i,j]
        else:
            print("Error: types or dimensions incompatibles.")
            result = None
        return result

    def concat(self, value, axis=1):
        if axis == 1 and self.shape[0] == value.shape[0]:
            result = zeros((self.shape[0], self.shape[1] + value.shape[1]))
            result[:,0:self.shape[1]] = self
            result[:,self.shape[1]:]  = value
        elif axis == 0 and self.shape[1] == value.shape[1]:
            result = zeros((self.shape[0] + value.shape[0], self.shape[1]))
            result[:self.shape[0],:] = self
            result[self.shape[0]:,:] = value
        else:
            print("Error: matrices with incompatible dimensions.")
            result = None
        return result
    
    def dot_operation(self, operation):
        result = zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[i,j] = operation(self[i,j])
        return result
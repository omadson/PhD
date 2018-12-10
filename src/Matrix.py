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
    

    def __item2list__(self, i,j):
        list_index = [0,0]
        for dim,count in [(i,0),(j,1)]:
            if type(dim) is int:
                list_index[count] = [self.shape[count] + dim if dim < 0 else dim]

            if type(dim) is slice:
                start = 0 if dim.start == None else dim.start
                step  = 1 if dim.step == None else dim.step
                stop = self.shape[count] if dim.stop == None else dim.stop
                step = -1 if start > stop and step == 1 else step

                if stop > start and step < 0: stop, start = start, stop-1

                list_index[count] = list(range(start, stop,step))

            if type(dim) is Matrix: dim = dim.transpose().linhas[0] if dim.shape[0] > dim.shape[1] else dim.linhas[0]
            if type(dim) is list: list_index[count] = [i.linhas[0] if type(i) is Matrix else i for i in dim]
        return list_index


    def __getitem__(self, item):
        i,j = item
        if type(i) is int and type(j) is int:
            return self.linhas[i][j]

        list_index = self.__item2list__(i,j)

        result = list()
        for row in list_index[0]:
            aux_list = list()
            for col in list_index[1]:
                aux_list.append(self.linhas[row][col])
            result.append(aux_list)

        return Matrix(result)
    
                
    def __setitem__(self, item, value):
        i, j = item
        if type(i) is int and type(j) is int:
            self.linhas[i][j] = value
        else:

            list_index = self.__item2list__(i, j)

            if type(value) is int:
                value = ones((len(list_index[0]), len(list_index[1]))) * value

            row_ = 0
            col_ = 0
            for row in list_index[0]:
                for col in list_index[1]:
                    self[row,col] = value[row_,col_]
                    col_ += 1
                row_ += 1

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
                for i in range(self.shape[1]): result = result + self[0,i] * value[i,0]
            else:
                result = zeros((self.shape[0], value.shape[1]))
                for i in range(self.shape[0]):
                    for j in range(value.shape[1]):
                        result[i,j] = self[i,:] * value[:,j]
        return result

    def __abs__(self): return self.__dot_operation__(abs)

    def transpose(self):
        result = zeros((self.shape[1], self.shape[0]))
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[j,i] = self[i,j]
        return result

    def __operation__(self, operation, axis=0, arg=0):
        operations_list = {'sum': sum, 'min': min, 'max': max}
        result = list()
        if axis == 1:
            for i in range(self.shape[0]):
                if arg == 0: result.append([operations_list[operation](self.linhas[i])])
                else: result.append([self.linhas[i].index(operations_list[operation](self.linhas[i]))])
        else:
            if arg == 0: return self.transpose().__operation__(operation, axis=1).transpose()
            else: return self.transpose().__operation__(operation, axis=1, arg=1).transpose()
        return Matrix(result)

    def sum(self, axis=0): return self.__operation__('sum', axis=axis)
    def max(self, axis=0): return self.__operation__('max', axis=axis)
    def argmax(self, axis=0): return self.__operation__('max', axis=axis, arg=1)
    def min(self, axis=0): return self.__operation__('min', axis=axis)
    def argmin(self, axis=0): return self.__operation__('min', axis=axis, arg=1)





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
    
    def __dot_operation__(self, operation):
        result = zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[i,j] = operation(self[i,j])
        return result




    # def gauss_elimination(self):
    #     result = self
    #     _, n = self.shape
    #     for k in range(n):
    #         p = result[k:n-1,k].__dot_operation__(abs).argmax().linhas[0][0]
    #         p = p+k;
    #         print(result[[p,k],:])
    #         print(result[[k,p],:])
    #         result[[k,p],:] = result[[p,k],:] if p != k else result[[k,p],:]

    #         for i in range(k+1,n+1):# i=k+1:n
    #             # print(self[i,k], self[k,k])
    #             m = result[i,k] / result[k,k]
    #             print(result)    
    #             result[i,k:] = result[i,k:] - (result[k,k:] * m);
    #     return result
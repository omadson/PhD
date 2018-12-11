import math
import copy
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

# eye method
def eye(dimension):
    if type(dimension) is int:
        result = zeros(dimension)
        for i in range(result.shape[0]): result[i,i] = 1
        return result
    else:
        print("error: dimension not int")
        return False

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
                # step = -1 if start > stop and step == 1 else step

                if stop > start and step < 0: stop, start = start, stop-1
                stop = self.shape[count] + stop if stop < 0 else stop

                list_index[count] = list(range(start, stop,step))

            if type(dim) is Matrix: dim = dim.transpose().linhas[0] if dim.shape[0] > dim.shape[1] else dim.linhas[0]
            if type(dim) is set: dim = list(dim)
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
            for row in list_index[0]:
                col_ = 0
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
                result = copy.deepcopy(self)
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        result[i,j] = result[i,j] + value[i,j]
        elif type(value) in [int,float]:
            result = copy.deepcopy(self) + Matrix([[value]*self.shape[1]]*self.shape[0])
        return result

    def __sub__(self, value):
        if type(value) == Matrix:
            if self.shape != value.shape:
                print("Error: incompatible dimensions.")
                return False
            else:
                result = copy.deepcopy(self)
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        result[i,j] = result[i,j] - value[i,j]
        elif type(value) in [int,float]:
            result = copy.deepcopy(self) - Matrix([[value]*self.shape[1]]*self.shape[0])
        return result

    def __neg__(self):
        return self * (-1)

    def __mul__(self, value):
        result = copy.deepcopy(self)
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
            result[:,0:self.shape[1]] = copy.deepcopy(self)
            result[:,self.shape[1]:]  = value
        elif axis == 0 and self.shape[1] == value.shape[1]:
            result = zeros((self.shape[0] + value.shape[0], self.shape[1]))
            result[:self.shape[0],:] = copy.deepcopy(self)
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

    def power(self, n):
        return self.__dot_operation__(lambda x: pow(x,n))

    def to_number(self):
        if self.shape == (1,1):
            return self.linhas[0][0]

    def trace(self):
        return sum([self[i,i] for i in range(self.shape[0])]) if self.shape[0] == self.shape[1] else False
    
    def back_substituition(self):
        N, M = self.shape
        # vector of soluctions
        x = zeros((1,N))

        # auxiliary matrices
        A = self[:,:-1]
        b = self[:,-1]

        if sum([A[i,i] == 0 for i in range(N)]) == 0:
            x[0,N-1] = b[N-1,0] / A[N-1,N-1]
            for j in range(N-2,-1,-1):
                x[0,j] = (b[j,0] - A[j,j+1:].dot(x[0,j+1:]).sum(axis=1).to_number() ) / A[j,j]
            return x
        else:
            print("the system not can solved by back substituition.")
            return False
    def gauss_elimination(self):
        N, M = self.shape
        Ab_ = copy.deepcopy(self)
        # phase 1: convert A to a superior triangular matrix
        for n in range(N):
            pivot = Ab_[n,n]
            for i in range(n+1,N):
                f = Ab_[i,n] / pivot
                Ab_[i,:] = Ab_[i,:] - (Ab_[n,:] * f)
        # phase 2: solve the system using back substituition
        return Ab_.back_substituition()

    def lu_decomposition(self):
        N = self.shape[0]
        L = eye(N)
        U = copy.deepcopy(self)
        for n in range(N):
            L[n+1:,n] = U[n+1:,n] * (1/U[n,n])
            for l  in range(n+1,N):
                U[l,:] = U[l,:] - (U[n,:] * L[l,n])
        return L, U

    def chol_decomposition(self):
        N = self.shape[0]
        L = zeros(N)
        for i in range(N):
            L[i,i] = pow(- (L[i,:] * L[i,:].transpose()) + self[i,i], 1/2)
            for j in range(i+1,N):
                L[j,i] = (- (L[i,:] * L[j,:].transpose()) + self[j,i]) / L[i,i]
        return L

    def jacob(self, b, K):
        M  = self.shape[1]
        x_old = zeros((1,M))
        x_new = zeros((1,M))

        for k in range(K):
            x_old = copy.deepcopy(x_new)
            for i in range(M):
                list_index = set(range(M)) - {i}
                sum_1 = self[i,list_index].dot(x_old[0,list_index]).sum(axis=1).to_number()
                x_new[0,i] = (b[i,0] - sum_1) * (1 / self[i,i])
        return x_new

    def gauss_seidel(self, b, K):
        M  = self.shape[1]
        x_old = zeros((1,M))
        x_new = zeros((1,M))
        for k in range(K):
            x_old = copy.deepcopy(x_new)
            for i in range(M):

                sum_1 = self[i,:i].dot(x_new[0,:i]).sum(axis=1).to_number()
                sum_2 = self[i,i+1:].dot(x_old[0,i+1:]).sum(axis=1).to_number()
                x_new[0,i] = (b[i,0] - sum_1 - sum_2) * (1 / self[i,i])
        return x_new

    def successive_over_relaxation(self, b, K, omega):
        M  = self.shape[1]
        x_old = zeros((1,M))
        x_new = zeros((1,M))
        for k in range(K):
            x_old = copy.deepcopy(x_new)
            for i in range(M):

                sum_1 = self[i,:i].dot(x_new[0,:i]).sum(axis=1).to_number()
                sum_2 = self[i,i+1:].dot(x_old[0,i+1:]).sum(axis=1).to_number()
                
                x_new[0,i] = (1 - omega)*x_old[0,i] + (b[i,0] - sum_1 - sum_2) * (omega / self[i,i])
        return x_new

    def conjugate_gradients(self, b):
        M  = self.shape[1]
        x = b
        
        r = b - self * x
        p = copy.copy(r)

        rs_old = r.transpose() * r

        for i in range(M):
            Ap    = self * p

            alpha = rs_old / (p.transpose() * Ap)
            
            x = x + p * alpha
            r = r - Ap * alpha

            rs_new = r.transpose() * r
            if pow(rs_new,1/2) < 0.000001:
                return x
            p = r + p * (rs_new / rs_old)
            rs_old = rs_new

        return x.transpose()
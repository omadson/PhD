import numpy as np
import copy
from matplotlib import pyplot as plt
class Data:
    """docstring for Data"""
    def __init__(self, path='data.csv', delimiter=',', output_scheme='n'):
        self.path          = path
        self.delimiter     = delimiter
        self.output_scheme = output_scheme
    def split_io(self):
        if self.output_scheme == 'n':
            self.X = self.data[:,:-1]
            self.y = -1 + self.data[:,-1][np.newaxis].T
    def shuffle(self):
        np.random.shuffle(self.data)
        self.split_io()

    def load(self):
        self.data = np.loadtxt(self.path, delimiter=self.delimiter)
        self.split_io()
        
    def plot(self):
        if self.data.shape[1] == 2:
            plt.scatter(self.data[:,0], self.data[:,1])
            plt.title('Dataset')
            plt.xlabel('feature #1')
            plt.ylabel('output')
            plt.show()
        if self.data.shape[1] == 3:
            plt.scatter(self.data[:,0], self.data[:,1], c=self.data[:,2])
            plt.title('Dataset')
            plt.xlabel('feature #1')
            plt.ylabel('feature #2')
            plt.show()

        else:
            print("Plot error: Dataset with 3 or more features.")
    
    def copy(self):
        return copy.copy(self)

    def add_bias(self):
        if not(np.any(self.data[:,0] == 1)):
            data_bias = np.ones((self.data.shape[0],self.data.shape[1]+1))
            data_bias[:,1:] = self.data
            self.data = data_bias
            self.split_io()
import numpy as np
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
            self.y = self.data[:,-1][np.newaxis].T
    def shuffle(self):
        np.random.shuffle(self.data)
        self.split_io()

    def load(self):
        self.data = np.loadtxt(self.path, delimiter=self.delimiter)
        self.split_io()
        
    def plot(self):
        if self.data.shape[1] - 1 == 2:
            plt.scatter(self.data[:,-2], self.data[:,-1])
            plt.title('Dataset')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.show()

    def add_bias(self):
        self.data = np.concatenate((np.ones((self.data.shape[0],1)),self.data),1)
        self.split_io()
class Regressor(object):
    """docstring for Regressor"""
    def __init__(self, arg):
        super(Regressor, self).__init__()
        self.arg = arg

    def fit(self, X, y):
        pass    
    
    def predict(X):
        pass




import numpy as np
from matplotlib import pyplot as plt

class LinearRegressor(Regressor):
    """docstring for LinearRegressor"""
    def __init__(self, method="OLS", params={'eta': 0.01, 'epochs': 100}):
        self.method  = method
        self.params  = params
        self.model   = dict()
        self.metrics = dict()

    def fit(self, data):
        self.train_data = data

        # ordinary least squares
        if self.method == 'OLS':
            self.model['w'] = np.linalg.pinv(data.X).dot(data.y)
            self.metrics['mse'] = np.power(data.y - data.X.dot(self.model['w']),2).mean()
        
        # gradient descendent
        elif self.method == 'GD':
            self.model['w']     = 0.01 * np.random.randn(data.X.shape[1],1)
            self.metrics['mse'] = np.zeros((self.params['epochs'],))
            y_hat               = data.X.dot(self.model['w'])
            for i in range(self.params['epochs']):
                self.model['w']        = self.model['w'] + self.params['eta'] * np.mean(np.multiply(data.y - y_hat, data.X),0)[np.newaxis].T + \
                                         
                y_hat                  = data.X.dot(self.model['w'])
                # mean squared error
                self.metrics['mse'][i] = ((data.y - y_hat) ** 2).mean()

        # stochastic gradient descendent
        elif self.method == 'SGD':
            self.model['w'] = 0.01 * np.random.randn(data.X.shape[1],1)
            self.metrics['mse'] = np.zeros((self.params['epochs'],))
            for i in range(self.params['epochs']):
                for j in range(data.X.shape[0]):
                    y_hat_j         = data.X[j,:].dot(self.model['w'])
                    self.model['w'] = self.model['w'] + self.params['eta'] * np.multiply(data.y[j,:] - y_hat_j, data.X[j,:])[np.newaxis].T
                # mean squared error
                y_hat                  = data.X.dot(self.model['w'])
                self.metrics['mse'][i] = ((data.y - y_hat) ** 2).mean()
                data.shuffle()

    def predict(self, X):
        return X.dot(self.model['w'])

    def plot(self, info='curve'):
        if info == 'curve':
            
            X_ = np.array([np.min(self.train_data.X,0), np.max(self.train_data.X,0)])
            plt.title('Linear approximation')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.scatter(self.train_data.X[:,1], self.train_data.y)
            plt.plot(X_[:,1], self.predict(X_), 'k-')
            plt.show()
        elif info == 'mse':
            plt.plot(range(self.params['epochs']), self.metrics['mse'])
            plt.title('Mean Squared Error (w = [%.3f, %.3f])' % (self.model['w'][0], self.model['w'][1]))
            plt.xlabel('Epochs')
            plt.ylabel('MSE')
            plt.show()


        
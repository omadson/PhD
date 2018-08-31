class Classification(object):
    """docstring for Regression"""
    def __init__(self, arg):
        self.arg = arg

    def fit(self, X, y):
        pass    
    
    def predict(X):
        pass

from numpy.linalg import inv
from numpy.random import randn
from numpy import dot, eye, ones, zeros, mean, meshgrid, arange, multiply, power, newaxis, min, max, array, exp, c_, squeeze
from matplotlib import pyplot as plt

class LogisticRegression(Classification):
    """docstring for LogisticRegression"""
    def __init__(self, params={'method':'OLS', 'lambda': 0}):
        self.params  = params
        self.model   = dict()
        self.metrics = dict()

        params['lambda'] = 0 if 'lambda' not in self.params.keys() else params['lambda']
        if self.params['method'] in ['SGD', 'GD']:
            params['eta']    = 0.01 if 'eta' not in self.params.keys() else params['eta']
            params['epochs'] = 100 if 'epochs' not in self.params.keys() else params['epochs']

    def fit(self, data):
        self.train_data = data.copy()
        # self.train_data.add_bias()
        X_ = self.train_data.X
        y_ = self.train_data.y
        # initial estimation of w
        w = 0.01 * randn(X_.shape[1],1)
        # ordinary least squares with regularization
        if self.params['method'] == 'GD':
            self.metrics['mse_i'] = zeros((self.params['epochs'],))
            y_hat               = self.predict_value(X_, w)
            for i in range(self.params['epochs']):
                # bias update
                w[0]     = w[0] + self.params['eta'] * mean(y_ - y_hat)
                # weigth update
                w[1:]    = w[1:] + self.params['eta'] * (mean(multiply(y_ - y_hat, X_[:,1:]),0)[newaxis].T - \
                                         self.params['lambda']/X_.shape[0]*w[1:])
                y_hat                  = self.predict_value(X_, w)
                # mean squared error
                self.metrics['mse_i'][i] = mean((y_ - y_hat) ** 2)

        # stochastic gradient descendent
        elif self.params['method'] == 'SGD':
            self.metrics['mse_i'] = zeros((self.params['epochs'],))
            for i in range(self.params['epochs']):
                for j in range(X_.shape[0]):
                    y_hat_j         = self.predict_value(X_[j,:], w)
                    w = w + self.params['eta'] * multiply(y_[j,:] - y_hat_j, X_[j,:])[newaxis].T 
                # mean squared error
                y_hat                  = dot(X_,w)
                self.metrics['mse_i'][i] = mean((y_ - y_hat) ** 2)
                data.shuffle()

        self.model['w']     = w
        self.metrics['mse'] = mean((y_ - dot(X_,self.model['w'])) ** 2)

    def predict_value(self, X, w=False):
        # X_bias = ones((X.shape[0],X.shape[1]+1))
        # X_bias[:,1:] = X
        if type(w) == bool:
            w = self.model['w']
        return 1 / (1 + exp(-dot(X,w)))

    def predict(self, X, w=False):
        # X_bias = ones((X.shape[0],X.shape[1]+1))
        # X_bias[:,1:] = X
        if type(w) == bool:
            w = self.model['w']
        return ((1 / (1 + exp(-dot(X,w)))) >= 0.5) * 1

    def plot(self,info='curve',X=False):
        if type(X) == bool:
            X = self.train_data.X
        if info == 'curve':
            # Parameters
            
            # plt.title('Decision surface (%s)\n(w=[%.3f, %.3f], MSE=%.3f)' % (self.params['method'],self.model['w'][0], self.model['w'][1], self.metrics['mse']))


            x_min, x_max = X[:, 1].min(), X[:, 1].max()
            y_min, y_max = X[:, 2].min(), X[:, 2].max()

            x_step = (x_max - x_min) / 200
            y_step = (y_max - y_min) / 200

            xx, yy = meshgrid(arange(x_min-10*x_step, x_max+10*x_step, x_step), arange(y_min-10*y_step, y_max+10*y_step, y_step))

            Z = self.predict(c_[ones(xx.ravel().shape[0]), xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)

            plt.contour(xx, yy, Z, [0.5], linewidths=1, colors='k')
            # print(X[:,1].shape)
            # print(X[:,2].shape)
            plt.scatter(X[:,1], X[:,2], c=squeeze(self.train_data.y))

            plt.xlabel('feature #1')
            plt.ylabel('feature #2')
            plt.show()
        elif info == 'mse':
            plt.plot(range(self.params['epochs']), self.metrics['mse_i'])
            plt.title('Mean Squared Error (%s)\n(w=[%.3f, %.3f], MSE=%.3f)' % (self.params['method'],self.model['w'][0], self.model['w'][1], self.metrics['mse']))
            plt.xlabel('Epochs')
            plt.ylabel('MSE')
            plt.show()
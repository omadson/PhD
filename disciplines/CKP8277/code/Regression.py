class Regression(object):
    """docstring for Regression"""
    def __init__(self, arg):
        super(Regression, self).__init__()
        self.arg = arg

    def fit(self, X, y):
        pass    
    
    def predict(X):
        pass


from numpy.linalg import inv
from numpy.random import randn
from numpy import dot, eye, mean, zeros, multiply, power, newaxis, min, max, array
from matplotlib import pyplot as plt

class LinearRegression(Regression):
    """docstring for LinearRegression"""
    def __init__(self, params={'method':'OLS', 'lambda': 0}):
        self.params  = params
        self.model   = dict()
        self.metrics = dict()

        # set default parameters
        #  - lambda (regularization parameter): 0
        #  - eta (learning rate): 0.01
        #  - epochs (number of epochs): 100
        params['lambda'] = 0 if 'lambda' not in self.params.keys() else params['lambda']
        if self.params['method'] in ['SGD', 'GD']:
            params['eta']    = 0.01 if 'eta' not in self.params.keys() else params['eta']
            params['epochs'] = 100 if 'epochs' not in self.params.keys() else params['epochs']
        

    def fit(self, data):
        self.train_data = data.copy()
        self.train_data.add_bias()
        X_ = self.train_data.X
        y_ = self.train_data.y
        # initial estimation of w
        w = 0.01 * randn(X_.shape[1],1)
        # ordinary least squares with regularization
        if self.params['method'] == 'OLS':
            lI = self.params['lambda'] * eye(X_.shape[1])
            lI[0,0] = 0
            w = dot(dot(inv(dot(X_.T,X_) + lI),X_.T), y_)

        
        # gradient descendent with regularization
        elif self.params['method'] == 'GD':
            self.metrics['mse_i'] = zeros((self.params['epochs'],))
            y_hat               = dot(X_,w)
            for i in range(self.params['epochs']):
                # bias update
                w[0]     = w[0] + self.params['eta'] * mean(y_ - y_hat)
                # weigth update
                w[1:]    = w[1:] + self.params['eta'] * (mean(multiply(y_ - y_hat, X_[:,1:]),0)[newaxis].T - \
                                         self.params['lambda']/X_.shape[0]*w[1:])
                y_hat                  = dot(X_, w)
                # mean squared error
                self.metrics['mse_i'][i] = mean((y_ - y_hat) ** 2)

        # stochastic gradient descendent
        elif self.params['method'] == 'SGD':
            self.metrics['mse_i'] = zeros((self.params['epochs'],))
            for i in range(self.params['epochs']):
                for j in range(X_.shape[0]):
                    y_hat_j         = dot(X_[j,:],w)
                    w = w + self.params['eta'] * multiply(y_[j,:] - y_hat_j, X_[j,:])[newaxis].T 
                # mean squared error
                y_hat                  = dot(X_,w)
                self.metrics['mse_i'][i] = mean((y_ - y_hat) ** 2)
                data.shuffle()

        self.model['w']     = w
        self.metrics['mse'] = mean((y_ - dot(X_,self.model['w'])) ** 2)      #np.power(y_ - X_.dot(self.model['w']),2).mean()

    def predict(self, X):
        return dot(X,self.model['w'])

    def plot(self, info='curve'):
        if info == 'curve':
            
            X_ = array([min(self.train_data.X,0), max(self.train_data.X,0)])
            plt.title('Linear approximation (%s)\n(w=[%.3f, %.3f], MSE=%.3f)' % (self.params['method'],self.model['w'][0], self.model['w'][1], self.metrics['mse']))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.scatter(self.train_data.X[:,1], self.train_data.y)
            plt.plot(X_[:,1], self.predict(X_), 'k-')
            plt.show()
        elif info == 'mse':
            plt.plot(range(self.params['epochs']), self.metrics['mse_i'])
            plt.title('Mean Squared Error (%s)\n(w=[%.3f, %.3f], MSE=%.3f)' % (self.params['method'],self.model['w'][0], self.model['w'][1], self.metrics['mse']))
            plt.xlabel('Epochs')
            plt.ylabel('MSE')
            plt.show()


        
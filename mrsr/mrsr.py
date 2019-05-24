import numpy as np
import itertools

def PRESS(D_in,D_out,W):
    D = D_out.shape[1]
    error = np.zeros(D)
    for d in range(D):
        error = (np.divide(D_out[:,d] - D_in @ W[:,d], 1 - np.diag(D_in @ np.linalg.inv(D_in.T @ D_in) @ D_in.T)) ** 2).mean()
    return error.mean()

def p_inv(X, X_pinv, x_k):
    d_k    = X_pinv @ x_k
    c_k    = x_k - X @ d_k
    k1     = np.linalg.inv(1 + d_k.T @ d_k)
    ckTck = c_k.T @ c_k
    c_k_pinv = np.linalg.inv(ckTck) @ c_k.T
    ck_Tck = c_k_pinv @ c_k
    XX = (1 - ck_Tck) @ k1 @ d_k.T @ X_pinv
    return np.vstack((X_pinv - d_k @ c_k_pinv - d_k @ XX, c_k_pinv + XX  ))

class MRSR(object):
    """docstring for MRSR"""
    def __init__(self, norm=1, feature_number=None,repetition_number=10,press=False,tol=None, pinv=True):
        self.norm  = norm
        self.max_k = feature_number
        self.n_var = repetition_number
        self.tol   = tol
        self.press = press
        self.pinv  = pinv
    
    def fit(self, X, T):

        n, m = X.shape
        q    = T.shape[1]

        c_k = np.zeros(m)
        W_k = np.zeros((m,q))
        # A = set()
        Y_k     = X @ W_k

        error = list()
        order = list()
        corr  = list()

        # optimization loop
        self.max_k = range(m-1) if self.max_k == None else range(self.max_k)
        
        if self.norm == 1: S = np.array(list(itertools.product([-1, 1], repeat=q)))

        for k in self.max_k:
            # compute correlation beetween inputs and outputs
            C_k        = (T - Y_k).T @ X
            c_k        = np.array([np.linalg.norm(C_k[:,j],self.norm) for j in range(m)])
            c_k[order] = 0
            c_k_hat    = c_k.max()
            corr.append(c_k_hat)
            # A       = A.union({c_k_hat})

            # add column most important to input vector
            i_max = int(c_k.argmax())
            order.append(i_max)
            X_k     = X[:,order]
            
            # estimate the regression coefficients
            if self.pinv==True:
                X_pinv = np.linalg.inv(X_k.T @ X_k) @ X_k.T if k == 0 else p_inv(X_k[:,:-1], X_pinv, X_k[:,-1][np.newaxis].T)
            else:
                X_pinv = np.linalg.inv(X_k.T @ X_k) @ X_k.T 

            W_k_hat = X_pinv @ T
            Y_k_hat = X_k @ W_k_hat
            
            
            # create W sparse
            W_k_hat_ = np.zeros((m,q))
            W_k_hat_[order,:] = W_k_hat


            # choice of lambda value

            U_k = C_k.copy()
            V_k = (Y_k_hat - Y_k).T @ X
            lb = list()
            if self.norm == np.inf:
                # Inf norm
                for j in set(range(m)).difference(set(order)):
                    u_kj = U_k[:,j]
                    v_kj = V_k[:,j]

                    a = (c_k_hat + u_kj) / (c_k_hat + v_kj)
                    b = (c_k_hat - u_kj) / (c_k_hat - v_kj)
                    LB = np.vstack((a,b))
                    lb.append(LB[LB>0].min())

            elif self.norm == 2:
                # l2 norm
                for j in set(range(m)).difference(set(order)):
                    u_kj = U_k[:,j]
                    v_kj = V_k[:,j]
                    uv_kj = v_kj.T @ u_kj
                    a = (v_kj.T @ v_kj) - c_k_hat**2
                    b = 2 * (c_k_hat**2 - uv_kj)
                    c = (u_kj.T @ u_kj) - c_k_hat**2

                    delta = b**2 - 4*a*c
                    if delta < 0:
                        pass
                    else:
                        if delta > 0:
                            x1 = (-b + np.sqrt(delta)) / (2*a)
                            x2 = (-b - np.sqrt(delta)) / (2*a)
                        elif delta == 0:
                            x1 = (-b) / (2*a)
                            x2 = x1
                        roots = np.array([x1,x2])
                        lb.extend(list(roots[roots > 0]))

            else:
                # l1 norm
                # create 
                for j in set(range(m)).difference(set(order)):
                    u_kj = U_k[:,j]
                    v_kj = V_k[:,j]
                    LB = list()
                    for s in S: LB.append((c_k_hat - s.T @ u_kj) / (c_k_hat - s.T @ v_kj))
                    LB = np.array(LB)
                    try:
                        lb.append(LB[LB>0].min())
                    except Exception as e:
                        lb.append(np.abs(LB).min())
            
            # if len(lb) == 0:
            #     return self
            lb_op = np.array(lb).min()

            # update o regression coefficients are 
            Y_k = ((1 - lb_op) * Y_k) + (lb_op * Y_k_hat)
            W_k = ((1 - lb_op) * W_k) + (lb_op * W_k_hat_)

            self.W     = W_k[order,:]
            self.order = list(order)
            self.error = error
            self.corr  = corr

            if k > self.n_var:
                if self.press == True:
                    error.append(PRESS(X,T,W_k))
                    error_var = np.std(np.array(error)[k-self.n_var:k])    
                    self.tol  = 10e-4 if self.tol == None else self.tol
                else:
                    error_var = np.std(np.array(corr)[k-self.n_var:k])
                    self.tol  = 0.5 if self.tol == None else self.tol

                if error_var < self.tol:
                    return self

        return self

    def predict(X):
        return X[:,order] @ self.W
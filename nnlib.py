import numpy as np
import pandas as pd
import copy
class nn:
    #Scaling function
    def scale(self,X):
        mean=np.mean(X,axis=0)
        var=np.var(X,axis=0)
        X=X-mean
        X/=(var)**0.5
        return X
    #Activation functions and their derivatives
    #Sigmoid
    def sigmoid(self,z):
        return 1/(1+(np.exp(-z)))
    def sigmoid_derivative(self,a):
        return self.sigmoid(a)*(1-self.sigmoid(a))
    
    #tanh
    def tanh(self,z):
        return (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))
    def tanh_derivative(self,a):
        return 1-self.tanh(a)**2
    
    #relu
    def relu(self,z):
        out=copy.deepcopy(z)
        out[out<0]=0
        return out
    def relu_derivative(self,a):
        out=copy.deepcopy(a)
        out[out>0]=1
        out[out<=0]=0
        return out
    
    #leaky_relu
    def leaky_relu(self,z,c=0.01):
        out=copy.deepcopy(z)
        return np.where(out>0, out, out * c)
    def leaky_relu_derivative(self,a,c=0.01):
        out=np.ones_like(a)
        out[a<0]=c
        return out
    
    #Softmax
    def softmax(self,z):
        t=np.exp(z)
        out=t/sum(t)
        return out
    #Softmax derivative(Not actually derivative but helper function to find dz)
    def softmax_derivative(self,y,a):
        return a-y
    
    #Loss function and its derivative
    def log_loss(self,y,a):
        return (-y *np.log(a+10**-8)-(1-y)*np.log(1 - a+10**-8)).mean()
    
    def log_loss_derivative(self,y,a):
        return (-y/a)+((1-y)/(1-a))
    
    #Random Weights Initialisation function
    def init_weights(self,nodes,features):
        return np.random.randn(nodes,features)
    
    
    def __init__(self,nodes, activations,features):
        # np.random.seed(0)
        self.nodes=nodes
        self.activations=activations    
        self.act_func={'sigmoid':self.sigmoid,'tanh':self.tanh,'relu':self.relu,'leaky_relu':self.leaky_relu,'softmax':self.softmax}
        self.act_func_der={'sigmoid':self.sigmoid_derivative,'tanh':self.tanh_derivative,'relu':self.relu_derivative,
                  'leaky_relu':self.leaky_relu_derivative,'softmax':self.softmax_derivative}
        self.w=[0]
        self.b=[0]
        for layer in range(len(self.nodes)):
            self.w.append(self.init_weights(self.nodes[layer],features))
            self.b.append(np.zeros((self.nodes[layer],1)))
            features=self.nodes[layer]
                
    def predict(self,X):
        X=self.scale(X)
        Layers_num=len(self.nodes)
        z=[0]
        a=[X]
        for layer in range(1,Layers_num+1):
            z.append(np.dot(self.w[layer],a[layer-1])+self.b[layer])
            a.append(self.act_func[self.activations[layer-1]](z[layer]))
        
        output=copy.deepcopy(a[-1])
        return output.T

'''=============================================================================================================================='''
'''=============================================================================================================================='''

#brain=nn([4,3],['relu','softmax'],4)
#input=np.array([1,2,3,4]).reshape(4,1)
#print(brain.predict(input))
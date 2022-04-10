''' Pricer for American Options
    Uses Binomial Tree Method
'''
import numpy as np

class American:
    # S: Spot Price
    # K: Strike Price
    # T: Time to maturity in years
    # sigma: Volatility 
    # r: Risk Free Rate
    # N: number of steps in Binomial Tree
    # option_type: call or put
    def __init__(self, S=None, K=None, T=0, sigma=None, r=0, N=200, option_type=None):
        assert option_type=='call' or option_type=='put'
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.N = N
        self.option_type= option_type

    def binomial_tree(self):
        S, K, T, sigma, N, r, option_type = self.S, self.K, self.T, self.sigma, self.N, self.r, self.option_type

        dT = T/N # size of time step
        DF = np.exp(-r*dT) # Discount Factor

        # u and d determined using Coxx-Rubinstein-Ross Approach
        u = np.exp(sigma*np.sqrt(dT))
        d = 1/u
        p = ((1/DF) - d)/(u-d) # Probability of Up or Down movements

        stock_prices = np.asarray([(S* d**j * u**(N-j)) for j in range(N+1)]) # Initalize stock price at the leaf

        # Initialize option price at the leaf
        if option_type =='call':
            option_price = np.maximum(stock_prices - K,0)
        else:
            option_price = np.maximum(K - stock_prices,0)

        # Calculate option price at each time step
        for i in range(N):
            stock_prices=stock_prices[:-1]*d
            option_price = DF*p*option_price[:-1] + DF*(1-p)*option_price[1:]
    
            if option_type == 'call':
                option_price = np.maximum(stock_prices-K,option_price)
            else:
                option_price = np.maximum(K-stock_prices,option_price)

        return option_price[0]

#a = American(50,52,2,0.223144,0.05,500,'put')
#print(a.binomial_tree())

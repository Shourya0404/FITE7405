''' Pricer for Geometric and Arithmetic Asian Options
    Geometric: Closed form solution
    Arithmetic: Monte Carlo and Control Variate (using Geometric) solutions 
'''
from math import sqrt, log,exp
from scipy.stats import norm
import numpy as np

class Asian:

    # S: Spot Price
    # K: Strike Price
    # T: Time to maturity in years
    # sigma: Volatility 
    # r: Risk Free Rate
    # n: number of observation times
    # M: number of paths in Monte Carlo simulation
    # control_variate: Using control variate or not
    # option_type: call or put
    def __init__(self, S=None, K=None, T=0, sigma=None, r=0, n=100, option_type=None, M = 10**5,control_variate=False):
        assert option_type=='call' or option_type=='put'
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.n = n
        self.M = M
        self.option_type= option_type
        self.control_variate =  control_variate


    def geometric_asian(self):
        N= norm.cdf
        S, K, T, sigma, n, r, option_type = self.S, self.K, self.T, self.sigma, self.n, self.r, self.option_type
        sigmaSqT = sigma**2 * T * (n+1)*(2*n +1)/(6*n*n)
        muT = 0.5*sigmaSqT + (r - 0.5*sigma**2)*T*(n + 1)/(2*n)

        d1 = (log(S/K) + (muT + 0.5*sigmaSqT))/(sigmaSqT**0.5)
        d2 = d1 - sqrt(sigmaSqT)
        
        if option_type =='call':
            N1 = N(d1)
            N2 = N(d2)

            call_price = exp(-1*r*T)*(S*exp(muT)*N1 - K*N2) # Closed form formula for Geometric Asian Call

            return call_price
        else:
            N1 = N(-1*d1)
            N2 = N(-1*d2)

            put_price = exp(-1*r*T)*(K*N2 -S*exp(muT)*N1) # Closed form formula for Geometric Asian Put
            return put_price 

    # Generates sample of Monte Carlo paths by taking random numbers from a standard normal
    def price_path(self,S,T,sigma,r,n,M):
        Dt=T/n
        np.random.seed(100)
        Z = np.random.randn(M,n)
        drift = (r- 0.5 * sigma**2)*Dt # Drift parameter of Brownian motion
        vol = sigma * np.sqrt(Dt) # Volatility parameter of Brownian motion
        price_path = S* np.cumprod(np.exp(drift + (vol*Z)),1) # Generate random samples from standard normal, find cumulative product to generate price path
        
        return price_path

    def arithmetic_asian(self):

        S, K, T, sigma, n, r, option_type, M, control_variate = self.S, self.K, self.T, self.sigma, self.n, self.r, self.option_type, self.M, self.control_variate
        sPath = self.price_path(S,T,sigma,r,n,M) # Generate price paths for Monte Carlo

        arithMean = np.mean(sPath,1) # Arithmetic mean of price path

        # Payoff of arithmetic price path depending on option type
        if option_type=='call':
            arithPayoff = exp(-1*r*T)*np.maximum(np.subtract(arithMean,K), 0)
        else:
            arithPayoff = exp(-1*r*T)*np.maximum(np.subtract(K,arithMean), 0)
        # Using standard Monte Carlo 
        if not control_variate:
            Pmean = np.mean(arithPayoff) # Average of arithmetic payoff
            Pstd = np.std(arithPayoff) # Standard deviation of arithmetic payoff
            confmc = [Pmean-1.96*Pstd/sqrt(M), Pmean+1.96*Pstd/sqrt(M)] # 95% confidence interval of standad MC arithmetic asian price
            return Pmean, confmc

        # Using Geometric Option as Control Variate
        else:
            geoMean = np.exp(1/n*np.sum(np.log(sPath),1)) # Geometric mean of price path
            # Payoff of geometric price path depending on option type
            if option_type=='call':
                geoPayoff = exp(-1*r*T)*np.maximum(np.subtract(geoMean,K), 0)
            else:
                geoPayoff = exp(-1*r*T)*np.maximum(np.subtract(K,geoMean), 0)
            geo=self.geometric_asian() #Closed form payout

            # Convert arrays to 2D Shape to avoid memory allocation issue
            geoPayoff=geoPayoff.reshape(geoPayoff.shape[0],1)
            arithPayoff=arithPayoff.reshape(arithPayoff.shape[0],1)

            # If payoff is 0 for all paths return 0 as the price
            if np.var(geoPayoff) == 0:
                return 0,[0,0]

            # Calculate theta using sample coveriance
            covXY = np.mean(np.multiply(arithPayoff,geoPayoff))- np.mean(arithPayoff)*np.mean(geoPayoff)
            theta = covXY/np.var(geoPayoff)
            Z = arithPayoff + theta * (geo - geoPayoff) # Arithmetic payoff according to control variate
            Zmean = np.mean(Z) # Average of control variate payoff
            Zstd = np.std(Z) # Standard deviation of control variate payoff
            confcv = [Zmean-1.96*Zstd/sqrt(M), Zmean+1.96*Zstd/sqrt(M)] # 95% confidence interval of control variate arithmetic asian price
            return Zmean, confcv

#a = Asian(50,60,0.5,0.11,0.01,50,'call',10**5,True)
#print(a.arithmetic_asian())
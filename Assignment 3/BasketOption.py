''' Pricer for Geometric and Arithmetic Basket Options
    Geometric: Closed form solution
    Arithmetic: Monte Carlo and Control Variate (using Geometric) solutions 
'''
from math import sqrt, log,exp
from scipy.stats import norm
import numpy as np

class Basket:

    # S: Spot Price List
    # K: Strike Price
    # T: Time to maturity in years
    # sigma1: Volatility List
    # r: Risk Free Rate
    # rho: Correlation 
    # M: number of paths in Monte Carlo simulation
    # control_variate: Using control variate or not
    # option_type: call or put
    def __init__(self, S= None, K=None, T=0, sigma=None, r=0, rho= None, option_type=None, M= 10**5,control_variate=False):
        assert option_type=='call' or option_type=='put'
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.rho = rho
        self.M = M
        self.option_type= option_type
        self.control_variate =  control_variate


    def geometric_basket(self):
        N= norm.cdf
        S, K, T, sigma, r, rho, option_type = self.S, self.K, self.T, self.sigma, self.r, self.rho, self.option_type

        S= np.array(S)

        n=len(S) # Number of assets in basket
        B = np.exp(1/n*np.sum(np.log(S))) # Geometric Mean of Assets

        sigma = np.array(sigma)
 
        rho_matrix = np.array([1,rho])

        rho_matrix = rho_matrix[np.abs(np.arange(rho_matrix.size) - np.arange(rho_matrix.size)[:,None])] # Creating variance covariance matrix

        sigma_b = sqrt(np.matmul(np.matmul(sigma,rho_matrix),sigma))/n
        mu_b = r - (0.5*np.sum(np.square(sigma))/n) + (0.5*sigma_b**2)

        d1 = (log(B/K) + (mu_b + 0.5*sigma_b**2)*T)/ (sigma_b*sqrt(T))
        d2 = d1 - (sigma_b*sqrt(T))
 
        if option_type =='call':
            N1 = N(d1)
            N2 = N(d2)

            call_price = exp(-1*r*T)*(B*exp(mu_b*T)*N1 - K*N2) # Closed form formula for Geometric Asian Call

            return call_price
        else:
            N1 = N(-1*d1)
            N2 = N(-1*d2)

            put_price = exp(-1*r*T)*(K*N2 -B*exp(mu_b*T)*N1) # Closed form formula for Geometric Asian Put

            return put_price 

    # Generates sample of Monte Carlo paths by taking random numbers from a standard normal
    def price_path(self,S,T,sigma,r,M,rho,n=1):
        Dt=T/n
        np.random.seed(100)
        Z1 = np.random.randn(M,n)
        Z2 = Z1*rho+np.sqrt(1-rho**2)*np.random.randn(M,n)
        drift1 = (r- 0.5 * sigma[0]**2)*Dt # Drift parameter of Brownian motion
        drift2 = (r- 0.5 * sigma[1]**2)*Dt # Drift parameter of Brownian motion
        vol1 = sigma[0] * np.sqrt(Dt) # Volatility parameter of Brownian motion
        vol2 = sigma[1] * np.sqrt(Dt) # Volatility parameter of Brownian motion
        price_path1 = S[0]* np.exp(drift1 + (vol1*Z1)) # Generate random samples from standard normal, find cumulative product to generate price path
        price_path2 = S[1]* np.exp(drift2 + (vol2*Z2)) # Generate random samples from standard normal, find cumulative product to generate price path
        
        return price_path1,price_path2

    def arithmetic_basket(self):

        S, K, T, sigma, r, rho, option_type, M, control_variate = self.S, self.K, self.T, self.sigma, self.r, self.rho, self.option_type, self.M, self.control_variate

        n = len(S)
        S1Path,S2Path= self.price_path(S,T,sigma,r,M,rho) # Generate price paths for Monte Carlo

        arithMean= 1/n*(S1Path+S2Path) # Arithmetic mean of price path

        # Payoff of arithmetic price path depending on option type
        if option_type=='call':
            arithPayoff = exp(-1*r*T)*np.maximum(np.subtract(arithMean,K), 0)
        else:
            arithPayoff = exp(-1*r*T)*np.maximum(np.subtract(K,arithMean), 0)
        
        # Using standard Monte Carlo 
        if not control_variate:
            Pmean = np.mean(arithPayoff) # Average of arithmetic payoff
            Pstd = np.std(arithPayoff) # Standard deviation of arithmetic payoff
            confmc = [Pmean-1.96*Pstd/sqrt(M), Pmean+1.96*Pstd/sqrt(M)] # 95% confidence interval of standad MC arithmetic basket price
            return Pmean, confmc

        # Using Geometric Option as Control Variate
        else:
            geoMean = np.exp(1/n*np.sum(np.log(S1Path*S2Path),1)) # Geometric mean of price path
            # Payoff of geometric price path depending on option type
            if option_type=='call':
                geoPayoff = exp(-1*r*T)*np.maximum(np.subtract(geoMean,K), 0)
            else:
                geoPayoff = exp(-1*r*T)*np.maximum(np.subtract(K,geoMean), 0)
            geo=self.geometric_basket() #Closed form payout

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
            confcv = [Zmean-1.96*Zstd/sqrt(M), Zmean+1.96*Zstd/sqrt(M)] # 95% confidence interval of control variate arithmetic basket price
            return Zmean, confcv



#b=Basket([100,100],100,3,[0.3,0.3],0.05,0.5,'call',10**5,True)
#print(b.geometric_basket())
#print(b.arithmetic_basket())
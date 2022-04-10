from math import sqrt, log,exp,pi
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class BlackScholes:
    def __init__(self):
        pass
    def euro_vanilla(self,S,K,T,t,sigma,r,option_type):
        N=norm.cdf
        d1,d2=self.d1_d2(S,K,T,t,sigma,r,0)
        if option_type=="call":
            C=S*N(d1)- K*exp(-1*r*(T-t))*N(d2)
            return C
        if option_type=="put":
            P=K*exp(-1*r*(T-t))*N(-1*d2) - S*N(-d1)
            return P
    # Verify if option price satisifes Put-Call Parity  
    def verify(self,C,P,S,K,T,t,r):
        if C-P-S+(K*exp(-1*r*(T-t)))==0:
            return True
        else:
            return False
        
    def euro_dividend_and_borrowing_cost(self, S,K,T,t,sigma,r,q,option_type):
        N=norm.cdf
        d1,d2=self.d1_d2(S,K,T,t,sigma,r,q)
        if option_type=="call":
            C=S*exp(-1*q*(T-t))*N(d1)- K*exp(-1*r*(T-t))*N(d2)
            return C
        if option_type=="put":
            P=K*exp(-1*r*(T-t))*N(-1*d2) - S*exp(-1*q*(T-t))*N(-d1)
            return P
    # Verify if option price satisifes Put-Call Parity  
    def verify_dividend_and_borrowing_cost(self,C,P,S,K,T,t,r,q):
        if C-P-(S*exp(-1*q*(T-t)))+(K*exp(-1*r*(T-t)))==0:
            return True
        else:
            return False
    def d1_d2(self,S,K,T,t,sigma,r,q):
        d1= ((log(S/K) + (r-q)*(T-t))/(sigma*sqrt(T-t)))+0.5*sigma*sqrt(T-t)
        d2=d1-(sigma*sqrt(T-t))
        return (d1,d2)
    def vega(self,S,K,T,t,r,sigma,q):
        d1,d2=self.d1_d2(S,K,T,t,sigma,r,q)
        vega= S*exp(-1*q*(T-t))*sqrt(T-t)*exp(-1*0.5*d1*sigma**2)/sqrt(2*pi)
        return vega
    # Verify if option price satisifies Black Scholes Bound
    def verify_bounds(self,S,K,T,t,r,q,price,optionType):
        if optionType=='call':
            if price>=S*exp(-1*q*T)-K*exp(-1*r*T) and price<S*exp(-1*q*T):
                return True
            else:
                return False
        if optionType=='put':
            if price>=K*exp(-1*r*T)-S*exp(-1*q*T) and price<K*exp(-1*r*T):
                return True
            else:
                return False

def get_implied_volatility(S,K,T,t,r,q,Ctrue,optiontype):
    # Use Newton's method to calculate Implied Volatility
    #starting value
    sigmahat = sqrt(2*abs( (log(S/K) + (r-q)*(T-t))/(T-t) ) )
    tol = 1e-8; # Tolerance
    nmax = 1000  # Number of Iterations
    sigmadiff=1
    n=1
    sigma=sigmahat
    bs=BlackScholes() # Initialize an Option object
    while (sigmadiff>=tol and nmax>n):
        if optiontype=='call':
            C=bs.euro_dividend_and_borrowing_cost(S,K,T,t,sigma,r,q,'call')
        else:
            C=bs.euro_dividend_and_borrowing_cost(S,K,T,t,sigma,r,q,'put')
        d1=bs.d1_d2(S,K,T,t,sigma,r,q)[0]
        Cvega=bs.vega(S,K,T,t,r,sigma,q)
        increment= (C-Ctrue)/Cvega
        sigma=sigma-increment
        n=n+1
        sigmadiff=abs(increment)
    return sigma
    
bs=BlackScholes()

r=0.03
S=2
K=2
T=3
t=0
sigma=0.3
q=0
Ctrue=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
print(get_implied_volatility(S,K,T,t,r,q,Ctrue,'call'))
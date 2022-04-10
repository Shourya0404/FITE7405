from math import sqrt, log,exp,pi
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd

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
        

bs=BlackScholes()

# 1.1
print('1.1')
# Define parameters
S=50
K = 50
t = 0
T = 0.5
sigma = 0.2
r = 0.01

C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
print('Call Option Price:',C)

P=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
print('Put Option Price:',P)

# 1.2
print('1.2')
# Define Parameters
S = 50
K = 60
t = 0
T = 0.5
sigma = 0.2
r = 0.01

C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
print('Call Option Price:',C)

P=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
print('Put Option Price:',P)

# 1.3
print('1.3')
# Define Parameters
S = 50
K = 50
t = 0
T = 1.0
sigma = 0.2
r = 0.01

C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
print('Call Option Price:',C)

P=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
print('Put Option Price:',P)

# 1.4
print('1.4')
# Define Parameters
S = 50
K = 50
t = 0
T = 0.5
sigma = 0.3
r = 0.01

C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
print('Call Option Price:',C)

P=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
print('Put Option Price:',P)

# 1.5
print('1.5')
# Define Parameters
S = 50
K = 50
t = 0
T = 0.5
sigma = 0.2
r = 0.02

C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
print('Call Option Price:',C)

P=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
print('Put Option Price:',P)


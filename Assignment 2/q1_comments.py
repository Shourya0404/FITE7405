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

print('Call Option Price decreases as Strike Price Increases')
S = 50
t = 0
T = 0.5
sigma = 0.2
r = 0.01
price=[]
param=[]
for K in range(10,100,10):
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
    price.append(C)
    param.append(K)
    #print('Strike Price:',K,'Call Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Strike Price')
# naming the y axis
plt.ylabel('Call Option Price')
plt.show()

print("\n")
print("Put Option Price Increases as Strike Price Increases")
S = 50
t = 0
T = 0.5
sigma = 0.2
r = 0.01
price=[]
param=[]
for K in range(10,100,10):
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
    price.append(C)
    param.append(K)
    #print('Strike Price:',K,'Put Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Strike Price')
# naming the y axis
plt.ylabel('Put Option Price')
plt.show()

print("\n")
print("Call Option Price Increases as Maturity Increases")
S = 50
K= 50
t = 0
sigma = 0.2
r = 0.01
price=[]
param=[]
for T in range(1,40,1):
    T=T*0.2
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
    price.append(C)
    param.append(T)
    #print('Maturity:',T,'Call Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Maturity')
# naming the y axis
plt.ylabel('Call Option Price')
plt.show()

print("\n")
print("Put Option Price Increases as Maturity Increases")
S = 50
K= 50
t = 0
sigma = 0.2
r = 0.01
price=[]
param=[]
for T in range(1,40,1):
    T=T*0.2
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
    price.append(C)
    param.append(T)
    #print('Maturity:',T,'Put Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Maturity')
# naming the y axis
plt.ylabel('Put Option Price')
plt.show()

print("\n")
print("Call Option Price Increases as Volatility Increases")
S = 50
K= 50
t = 0
T=0.5
r = 0.01
price=[]
param=[]
for sigma in range(1,40,1):
    sigma=sigma*0.01
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
    price.append(C)
    param.append(sigma)
    #print('Volatility:',sigma,'Call Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Volatility')
# naming the y axis
plt.ylabel('Call Option Price')
plt.show()

print("\n")
print("Put Option Price Increases as Volatility Increases")
S = 50
K= 50
t = 0
T=0.5
r = 0.01
price=[]
param=[]
for sigma in range(1,40,1):
    sigma=sigma*0.01
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
    price.append(C)
    param.append(sigma)
    #print('Volatility:',sigma,'Put Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Volatility')
# naming the y axis
plt.ylabel('Put Option Price')
plt.show()

print("\n")
print("Call Option Price Increases as Risk Free Rate Increases")
S = 50
K= 50
t = 0
T=0.5
sigma=0.2
price=[]
param=[]
for r in range(1,40,1):
    r=r*0.01
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'call')
    price.append(C)
    param.append(r)
    #print('Risk Free Rate:',r,'Call Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Risk Free Rate')
# naming the y axis
plt.ylabel('Call Option Price')
plt.show()

print("\n")
print("Put Option Price Decreases as Risk Free Rate Increases")
S = 50
K= 50
t = 0
T=0.5
sigma=0.2
price=[]
param=[]
for r in range(1,40,1):
    r=r*0.01
    C=bs.euro_vanilla(S,K,T,t,sigma,r,'put')
    price.append(C)
    param.append(r)
    #print('Risk Free Rate:',r,'Put Option Price:',C)
plt.plot(param,price)
# naming the x axis
plt.xlabel('Risk Free Rate')
# naming the y axis
plt.ylabel('Put Option Price')
plt.show()


''' BlackScholes Pricing for European Options and Implied Volatility Calculator'''

from math import sqrt, log,exp,pi
from scipy.stats import norm

class BlackScholes:
    # S: Spot Price
    # K: Strike Price
    # T: Time to maturity in years
    # sigma: Volatility 
    # r: Risk Free Rate
    # q: Repo Rate
    # option_type: call or put
       
    # Calculate Black Scholes Option price
    def euro_vanilla(self,S,K,T,sigma,r,q,option_type,t=0):
        N=norm.cdf
        d1,d2=self.d1_d2(S,K,T,sigma,r,q,t)
        if option_type=="call":
            C=S*exp(-1*q*(T-t))*N(d1)- K*exp(-1*r*(T-t))*N(d2)
            return C
        if option_type=="put":
            P=K*exp(-1*r*(T-t))*N(-1*d2) - S*exp(-1*q*(T-t))*N(-d1)
            return P

    # Verify if option price satisifes Put-Call Parity  
    def verify(self,C,P,S,K,T,r,q,t=0):
        if C-P-(S*exp(-1*q*(T-t)))+(K*exp(-1*r*(T-t)))==0:
            return True
        else:
            return False

     # Calculate d1 and d2
    def d1_d2(self,S,K,T,sigma,r,q,t=0):
        d1= ((log(S/K) + (r-q)*(T-t))/(sigma*sqrt(T-t)))+0.5*sigma*sqrt(T-t)
        d2=d1-(sigma*sqrt(T-t))
        return (d1,d2)
    
    # Calculate Vega 
    def vega(self,S,K,T,r,sigma,q,t=0):
        d1,d2=self.d1_d2(S,K,T,sigma,r,q,t)
        vega= S*exp(-1*q*(T-t))*sqrt(T-t)*exp(-1*0.5*d1*sigma**2)/sqrt(2*pi)
        return vega
        
    def get_implied_volatility(self,S,K,T,r,q,Ctrue,optiontype,t=0):
        # Use Newton's method to calculate Implied Volatility

        # Check if given parameters satisfy the option price bounds
        if self.verify_bounds(S,K,T,r,q,Ctrue,optiontype):
            #starting value
            sigmahat = sqrt(2*abs( (log(S/K) + (r-q)*(T-t))/(T-t) ) )
            tol = 1e-8; # Tolerance
            nmax = 1000  # Number of Iterations
            sigmadiff=1
            n=1
            sigma=sigmahat
            while (sigmadiff>=tol and nmax>n):
                if optiontype=='call':
                    C=self.euro_vanilla(S,K,T,sigma,r,q,'call',t)
                else:
                    C=self.euro_vanilla(S,K,T,sigma,r,q,'put',t)
                Cvega=self.vega(S,K,T,r,sigma,q,t)
                increment= (C-Ctrue)/Cvega
                sigma=sigma-increment
                n=n+1
                sigmadiff=abs(increment)
            return sigma
        else:
            return "N/A. Parameters do not satisfy Black Scholes Bound"

    # Verify if option price satisifies Black Scholes Bound 
    def verify_bounds(self,S,K,T,r,q,price,optionType):
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

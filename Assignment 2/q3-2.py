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
    nmax = 10000  # Number of Iterations
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

def imp_vol(data,r,q,T,t,end_time):
    S=(data[(data['Symbol']==510050) & (data['LocalTime']<=end_time)].iloc[-1]['Ask1']+data[(data['Symbol']==510050) & (data['LocalTime']<=end_time)].iloc[-1]['Bid1'])/2
    imp_vol_df=pd.DataFrame(index=data['Strike'].dropna().unique(),columns=['BidVolP','AskVolP','BidVolC','AskVolC'])
    imp_vol_df.index.name='Strike'
    imp_vol_df.index.type=str
    for symbol in data['Symbol'].unique()[:-1]:
        instrument=data[(data['Symbol']==symbol) & (data['LocalTime']<=end_time)].dropna().iloc[-1]
        K=instrument['Strike']
        true_bid=instrument['Bid1']
        true_ask=instrument['Ask1']
        optionType=instrument['OptionType']
        if optionType=='C':
            optionType='call'
        elif optionType=='P':
            optionType='put'
        if bs.verify_bounds(S,K,T,t,r,q,true_bid,optionType):
            bidsigma=get_implied_volatility(S,K,T,t,r,q,true_bid,optionType)
            Cbid=bs.euro_dividend_and_borrowing_cost(S,K,T,t,bidsigma,r,q,optionType)
            imp_vol_df.loc[K]['BidVol'+optionType[0].upper()]=bidsigma
        if bs.verify_bounds(S,K,T,t,r,q,true_ask,optionType):
            asksigma=get_implied_volatility(S,K,T,t,r,q,true_ask,optionType)
            Cask=bs.euro_dividend_and_borrowing_cost(S,K,T,t,asksigma,r,q,optionType)
            imp_vol_df.loc[K]['AskVol'+optionType[0].upper()]=asksigma
    return imp_vol_df.sort_index()
    
bs=BlackScholes()

def plot(df,time):
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(time)
    axs[0, 0].plot(df.index, df.BidVolP)
    axs[0, 0].set_title("BidVolP")
    axs[1, 0].plot(df.index, df.BidVolC,'tab:orange')
    axs[1, 0].set_title("BidVolC")
    axs[1, 0].sharex(axs[0, 0])
    axs[0, 1].plot(df.index, df.AskVolP,'tab:green')
    axs[0, 1].set_title("AskVolP")
    axs[1, 1].plot(df.index, df.AskVolC,'tab:red')
    axs[1, 1].set_title("AskVolC")
    axs[1, 1].sharex(axs[0, 1])
    fig.tight_layout()
    plt.show()

instruments=pd.read_csv('instruments.csv')

marketdata=pd.read_csv('marketdata.csv')

merged_df=instruments.merge(marketdata,left_on='Symbol',right_on='Symbol')

r=0.04
q=0.2
t=0
T=(24-16)/365


end_time='2016-Feb-16 09:31'
df_931=imp_vol(merged_df,r,q,T,t,end_time)
df_931.to_csv('31.csv')

end_time='2016-Feb-16 09:32'
df_932=imp_vol(merged_df,r,q,T,t,end_time)
df_932.to_csv('32.csv')

end_time='2016-Feb-16 09:33'
df_933=imp_vol(merged_df,r,q,T,t,end_time)
df_933.to_csv('33.csv')

plot(df_931,'9:31')
plot(df_932,'9:32')
plot(df_933,'9:33')
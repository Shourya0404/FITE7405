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
        put_call_parity=C-P-(S*exp(-1*q*(T-t)))+(K*exp(-1*r*(T-t)))
        if put_call_parity==0:
            return True
        else:
            return put_call_parity
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

bs=BlackScholes()

def update_prices(df,data):
        strike=data['Strike']
        optionType=data['OptionType']
        bid = data['Bid1']
        ask=data['Ask1']
        df.loc[strike][optionType+'BidPrice']=bid
        df.loc[strike][optionType+'AskPrice']=ask
        return df

def put_call_arbitrage(option_price,etf_bid_price,etf_ask_price,arbitrage_df,time):
    q=0.2
    r=0.04
    t=0
    T=(24-16)/365
    transaction_cost=3.3
    # Case 1: Short sell put, Short-sell underlying, Buy Call, Buy Risk Free Bond
    C=option_price['CAskPrice']
    P=option_price['PBidPrice']
    S=etf_bid_price
    K=option_price.name
    if pd.isna(C) or pd.isna(P) or pd.isna(S):
        return arbitrage_df
    put_call_arbitrage=bs.verify_dividend_and_borrowing_cost(C,P,S,K,T,t,r,q)
    if put_call_arbitrage!=True:
        if put_call_arbitrage<0:
            if put_call_arbitrage*10000<-1*transaction_cost:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Put-Call Parity Short sell put, Short-sell underlying, Buy Call, Buy Risk Free Bond',1,put_call_arbitrage*-10000 - transaction_cost]
            else:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Put-Call Parity Short sell put, Short-sell underlying, Buy Call, Buy Risk Free Bond',0,put_call_arbitrage*-10000]
                
    # Case 2: Short sell call, Short-sell bond, Buy Put, Buy Underlying
    C=option_price['CBidPrice']
    P=option_price['PAskPrice']
    S=etf_ask_price
    K=option_price.name
    if pd.isna(C) or pd.isna(P) or pd.isna(S):
        return arbitrage_df
    put_call_arbitrage=bs.verify_dividend_and_borrowing_cost(C,P,S,K,T,t,r,q)
    if put_call_arbitrage!=True:
        if put_call_arbitrage>0:
            if put_call_arbitrage*10000>transaction_cost:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Put-Call Parity Short sell call, Short-sell bond, Buy Put, Buy Underlying',1,put_call_arbitrage*10000-transaction_cost]
            else:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Put-Call Parity Short sell call, Short-sell bond, Buy Put, Buy Underlying',0,put_call_arbitrage*10000]
    
    return arbitrage_df

def call_option_bound_arbitrage(option_price,etf_bid_price,etf_ask_price,arbitrage_df,time):
    q=0.2
    r=0.04
    t=0
    T=(24-16)/365
    transaction_cost=3.3
    
    # Case 1: Buy Call, Buy Risk Free Bond, Short Sell Underlying
    # For no arbitrage, C+K-S>=0 or S-K-C<0
    # Make non-zero return on day 0, and don't lose money at maturity
    # IF K>S: K-S
    # IF S=K: 0
    # IF S>K: S-K+K-S=0
    C=option_price['CAskPrice']
    S=etf_bid_price
    K=option_price.name
    if pd.isna(C) or pd.isna(S):
        return arbitrage_df
    portfolio_value=S*exp(-1*q*T)-K*exp(-1*r*T)-C
    if portfolio_value>0:
            if portfolio_value*10000>transaction_cost:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Call Bound',1,portfolio_value*10000-transaction_cost]
            else:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Call Bound',0,portfolio_value*10000]
    return arbitrage_df


def put_option_bound_arbitrage(option_price,etf_bid_price,etf_ask_price,arbitrage_df,time):
    q=0.2
    r=0.04
    t=0
    T=(24-16)/365
    transaction_cost=3.3
    
    # Case 1: Buy Put, Sell Risk Free Bond, Buy Underlying
    # For no arbitrage, P-K+S>=0 
    # Make non-zero return on day 0, and don't lose money at maturity
    # IF K>S: 0
    # IF K=S: 0
    # IF S>K: S-K > 0 
    P=option_price['PAskPrice']
    S=etf_ask_price
    K=option_price.name
    if pd.isna(P) or pd.isna(S):
        return arbitrage_df
    portfolio_value=K*exp(-1*r*T)-S*exp(-1*q*T) -P
    if portfolio_value>0:
            if portfolio_value*10000>transaction_cost:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Put Bound',1,portfolio_value*10000-transaction_cost]
            else:
                arbitrage_df.loc[len(arbitrage_df)]=[C,P,K,S,time,'Put Bound',0,portfolio_value*10000]
    return arbitrage_df


def vertical_spread_arbitrage(strike,option_price_df,arbitrage_df,time):
    q=0.2
    r=0.04
    t=0
    T=(24-16)/365
    transaction_cost=3.3
    # Case 1: Buy Lower Strike, Sell Higher Strike
    # For no arbitrage, C(K1)>=C(K2) or C(K1)-C(K2)>=0
    # Make non-zero return on day 0, and don't lose money at maturity
    # IF K1>=S: 0
    # IF K1<S<=K2: S-K1
    # IF S>K2: K2-K1 > 0 
    # If C(K2)>C(K1) Arbitrage will exist
    
    # Case 2: Buy Higher Strike, Buy Risk Free Bond Higher Strike, Sell Lower Strike, Sell Risk Free Bond Lower Strike
    # For no arbitrage, C(K1) + K1 - C(K2) -K2 < 0 or C(K2) - C(K1) + K2 - K1 > 0
    # Make non-zero return on day 0, and don't lose money at maturity
    # IF K1>=S: K2 - K1 >0
    # IF K1<S<=K2: -S + K1 + K2 - K1 = K2 -S >=0
    # IF S>K2: S - K2 - S + K1 + K2 - K1 = 0
    
    for _ in range(len(option_price_df)):
        if option_price_df.iloc[_].name==strike:
            continue
        elif option_price_df.iloc[_].name < strike:
            C11=option_price_df.iloc[_]['CAskPrice']
            K11=option_price_df.iloc[_].name
            C21=option_price_df.loc[strike]['CBidPrice']
            K21=strike
            C12=option_price_df.iloc[_]['CBidPrice']
            K12=option_price_df.iloc[_].name
            C22=option_price_df.loc[strike]['CAskPrice']
            K22=strike
        else:
            C21=option_price_df.iloc[_]['CBidPrice']
            K21=option_price_df.iloc[_].name
            C11=option_price_df.loc[strike]['CAskPrice']
            K11=strike
            C22=option_price_df.iloc[_]['CAskPrice']
            K22=option_price_df.iloc[_].name
            C12=option_price_df.loc[strike]['CBidPrice']
            K12=strike
        if pd.isna(C11) or pd.isna(C21):
            continue
        # Case 1
        portfolio_value=C21-C11
        if portfolio_value>0:
            if portfolio_value*10000>transaction_cost:
                arbitrage_df.loc[len(arbitrage_df)]=[(C11,C21),np.nan,(K11,K21),np.nan,time,'Vertical Spread Lower Bound',1,portfolio_value*10000-transaction_cost]
            else:
                arbitrage_df.loc[len(arbitrage_df)]=[(C11,C21),np.nan,(K11,K21),np.nan,time,'Vertical Spread Lower Bound',0,portfolio_value*10000]
        # Case 2
        if pd.isna(C12) or pd.isna(C22):
            continue
        portfolio_value= C12 - C22 - K22*exp(-1*r*(T-t)) + K12*exp(-1*r*(T-t))
        if portfolio_value>0:
            if portfolio_value*10000>transaction_cost:
                arbitrage_df.loc[len(arbitrage_df)]=[(C12,C22),np.nan,(K12,K22),np.nan,time,'Vertical Spread Upper Bound',1,portfolio_value*10000-transaction_cost]
            else:
                arbitrage_df.loc[len(arbitrage_df)]=[(C12,C22),np.nan,(K12,K22),np.nan,time,'Vertical Spread Upper Bound',0,portfolio_value*10000]
    return arbitrage_df

def non_negative_butterfly_spread_arbitrage(strike,option_price_df,arbitrage_df,time):
    q=0.2
    r=0.04
    t=0
    T=(24-16)/365
    transaction_cost=3.3
    
    # Consider 3 options with strikes K1, K2, and K3 where 0<K1<K2<K3
    
    # Buy C(K1), Sell C(K2), Buy C(K3)
    
    # For no arbitrage, aC(K1) - bC(K2) + (b-a)C(K3) > 0
    
    # Dividing by b:
    #                  (a/b)C(K1) - C(K2) + (1-a/b)C(K3) > 0
    
    # a/b = (K3-K2)/(K3-K1), aK3 -aK1 = bK3 - bK2, (a-b)K3= aK1 -bK2
    
    # Make non-zero return on day 0, and don't lose money at maturity
    
    # IF K1>=S: 0
    # IF K1<S<=K2: a(S-K1) > 0
    # IF K2<S<=K3: a(S-K1) -b(S-K2) = (a-b)S -aK1 + bK2= (a-b)S - (a-b)K3 = (a-b)(S-K3) > 0
    # IF S>K3: a(S-K1) -b(S-K2) + (b-a)(S-K3)= aS -bS +bS -aS - aK1 + bK2 - bK3 + aK3 = 0
    
    # Take updated call option as K1
    K1= strike
    C1= option_price_df.loc[strike]['CAskPrice']
    for _ in range(round(round(K1+0.05,2)*100),260,5):
        K2 = option_price_df.loc[round(_*0.01,2)].name
        C2 = option_price_df.loc[round(_*0.01,2)]['CBidPrice']
        
        for __ in range(round(round(K2+0.05,2)*100),265,5):
            K3 = option_price_df.loc[round(__*0.01,2)].name
            C3 = option_price_df.loc[round(__*0.01,2)]['CAskPrice']
            
            a_b= (K3-K2)/(K3-K1)
            
            portfolio_value = C2 - a_b*C1 - (1-a_b)*C3
            if portfolio_value>0:
                if portfolio_value*10000>transaction_cost:
                    arbitrage_df.loc[len(arbitrage_df)]=[(C1,C2,C3),np.nan,(K1,K2,K3),np.nan,time,'Non Negative Butterfly',1,portfolio_value*10000-transaction_cost]
                else:
                    arbitrage_df.loc[len(arbitrage_df)]=[(C1,C2,C3),np.nan,(K1,K2,K3),np.nan,time,'Non Negative Butterfly',0,portfolio_value*10000]
    
    
    # Take updated call option as K2
    K2= strike
    C2= option_price_df.loc[strike]['CBidPrice']
    for _ in range(180,round(round(K2,2)*100),5):
        K1 = option_price_df.loc[round(_*0.01,2)].name
        C1 = option_price_df.loc[round(_*0.01,2)]['CAskPrice']
        
        for __ in range(round(round(K2+0.05,2)*100),265,5):
            K3 = option_price_df.loc[round(__*0.01,2)].name
            C3 = option_price_df.loc[round(__*0.01,2)]['CAskPrice']
            
            a_b= (K3-K2)/(K3-K1)
            
            portfolio_value = C2 - a_b*C1 - (1-a_b)*C3
            if portfolio_value>0:
                if portfolio_value*10000>transaction_cost:
                    arbitrage_df.loc[len(arbitrage_df)]=[(C1,C2,C3),np.nan,(K1,K2,K3),np.nan,time,'Non Negative Butterfly',1,portfolio_value*10000-transaction_cost]
                else:
                    arbitrage_df.loc[len(arbitrage_df)]=[(C1,C2,C3),np.nan,(K1,K2,K3),np.nan,time,'Non Negative Butterfly',0,portfolio_value*10000]
    
    
    # Take updated call option as K3
    K3= strike
    C3= option_price_df.loc[strike]['CAskPrice']
    for _ in range(180,round(round(K3-0.05,2)*100),5):
        K1 = option_price_df.loc[round(_*0.01,2)].name
        C1 = option_price_df.loc[round(_*0.01,2)]['CAskPrice']
        
        for __ in range(round(round(K1+0.05,2)*100),round(round(K3,2)*100),5):
            K2 = option_price_df.loc[round(__*0.01,2)].name
            C2 = option_price_df.loc[round(__*0.01,2)]['CBidPrice']
            
            a_b= (K3-K2)/(K3-K1)
            
            portfolio_value = C2 - a_b*C1 - (1-a_b)*C3
            if portfolio_value>0:
                if portfolio_value*10000>transaction_cost:
                    arbitrage_df.loc[len(arbitrage_df)]=[(C1,C2,C3),np.nan,(K1,K2,K3),np.nan,time,'Non Negative Butterfly',1,portfolio_value*10000-transaction_cost]
                else:
                    arbitrage_df.loc[len(arbitrage_df)]=[(C1,C2,C3),np.nan,(K1,K2,K3),np.nan,time,'Non Negative Butterfly',0,portfolio_value*10000]
     
    return arbitrage_df

instruments=pd.read_csv('instruments.csv')
marketdata=pd.read_csv('marketdata.csv')
merged_df=instruments.merge(marketdata,left_on='Symbol',right_on='Symbol')
marketdata=merged_df.sort_values('LocalTime').reset_index(drop=True)
etf_bid_price=np.nan
etf_ask_price=np.nan
latest_price_df=pd.DataFrame(index=merged_df['Strike'].dropna().unique(),columns=['CBidPrice','CAskPrice','PBidPrice','PAskPrice'])
latest_price_df.sort_index(inplace=True)
latest_price_df.index.name='Strike'
arbitrage_df=pd.DataFrame(columns=['CallPrice','PutPrice','StrikePrice','A50Price','LocalTime','Type','TransactionArbitrage','Profit'])
for _ in range(len(marketdata)):
    data=marketdata.iloc[_]
    if data['Type']=='Option':
        latest_price_df=update_prices(latest_price_df,data)
        arbitrage_df=put_call_arbitrage(latest_price_df.loc[data['Strike']],etf_bid_price,etf_ask_price,arbitrage_df,data['LocalTime'])
        arbitrage_df=call_option_bound_arbitrage(latest_price_df.loc[data['Strike']],etf_bid_price,etf_ask_price,arbitrage_df,data['LocalTime'])
        arbitrage_df=put_option_bound_arbitrage(latest_price_df.loc[data['Strike']],etf_bid_price,etf_ask_price,arbitrage_df,data['LocalTime'])
        if data['OptionType']=='C':
            arbitrage_df=vertical_spread_arbitrage(data['Strike'],latest_price_df,arbitrage_df,data['LocalTime'])
            arbitrage_df=non_negative_butterfly_spread_arbitrage(data['Strike'],latest_price_df,arbitrage_df,data['LocalTime'])
    else:
        etf_bid_price=data['Bid1']
        etf_ask_price=data['Ask1']

print("The following arbitrage opportunities exist")
print(arbitrage_df['Type'].value_counts())
print('\n')
print("The number of arbitrage opportunities including transaction cost:",len(arbitrage_df[arbitrage_df['TransactionArbitrage']==1]))
print("The total profit for cases involving transaction cost:",round(sum(arbitrage_df['Profit'][arbitrage_df['TransactionArbitrage']==1]),2))
print("The total profit for cases without transaction cost:",round(sum(arbitrage_df['Profit'][arbitrage_df['TransactionArbitrage']==0]),2))
arbitrage_df.to_csv('arbitrage_opportunities.csv')
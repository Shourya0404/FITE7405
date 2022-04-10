''' Test Cases for Asian, Basket, and American Options
    Results generated can be found in Option_Type_Tests.csv files
'''

import sys
import os
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

from AsianOption import Asian
from BasketOption import Basket
from AmericanOption import American
import pandas as pd

# Fixed parameters
r = 0.05
T =3 
S = 100
M = 10**5


# Testing Asian Options
asian_tests = [[100, 0.3 , 50],[100,0.3,100],[100,0.4,50]]

asian_data = pd.DataFrame(columns=['S','K','T', 'sigma', 'r', 'n', 'option_type','M', 'Geometric', 'Arithmetic MC','MC Confidence Interval', 'Arithmetic Control Variate','Control Variate Confidence Interval'])
for test in asian_tests:
    K = test[0]
    sigma = test[1]
    n = test[2]
    for option_type in ['call','put']:
        asian_data.loc[len(asian_data)]=[S,K,T,sigma,r,n,option_type,M,0,0,0,0,0]
        a = Asian(S, K , T, sigma, r , n, option_type, M)
        a_geo = a.geometric_asian()
        asian_data.at[len(asian_data)-1,'Geometric']=a_geo
        for control_variate in [True,False]:
            a.control_variate = control_variate
            a_arith = a.arithmetic_asian()
            if control_variate:
                asian_data.at[len(asian_data)-1,'Arithmetic Control Variate']=a_arith[0]
                asian_data.at[len(asian_data)-1,'Control Variate Confidence Interval']=a_arith[1]
            else:
                asian_data.at[len(asian_data)-1,'Arithmetic MC']=a_arith[0]
                asian_data.at[len(asian_data)-1,'MC Confidence Interval']=a_arith[1]
asian_data.to_csv('Asian_Tests.csv',index= False)

# Testing Basket Options
basket_tests = [[100, [0.3,0.3], 0.5] , [100, [0.3,0.3], 0.9], [100, [0.1,0.3], 0.5], [80, [0.3, 0.3], 0.5], [120, [0.3,0.3], 0.5], [100, [0.5,0.5], 0.5]]
basket_data = pd.DataFrame(columns=['S1','S2','K','T', 'sigma1','sigma2', 'r', 'rho', 'option_type','M', 'Geometric', 'Arithmetic MC', 'MC Confidence Interval','Arithmetic Control Variate','Control Variate Confidence Interval'])
for test in basket_tests:
    K = test[0]
    sigma = test[1]
    rho = test[2]
    for option_type in ['call','put']:
        basket_data.loc[len(basket_data)]=[S,S,K,T,sigma[0],sigma[1],r,rho,option_type,M,0,0,0,0,0]
        b = Basket([S,S], K, T, sigma, r, rho, option_type, M)
        b_geo = b.geometric_basket()
        basket_data.at[len(basket_data)-1,'Geometric']=b_geo
        for control_variate in [True,False]:
            b.control_variate = control_variate
            b_arith = b.arithmetic_basket()
            if control_variate:
                basket_data.at[len(basket_data)-1,'Arithmetic Control Variate']=b_arith[0]
                basket_data.at[len(basket_data)-1,'Control Variate Confidence Interval']=b_arith[1]
            else:
                basket_data.at[len(basket_data)-1,'Arithmetic MC']=b_arith[0]
                basket_data.at[len(basket_data)-1,'MC Confidence Interval']=b_arith[1]
basket_data.to_csv('Basket_Tests.csv', index=False)

# Testing American Options
S = 50
sigma = 0.4
r = 0.1
n = 200
T = 2
 
american_tests = [40,50,70]
american_data = pd.DataFrame(columns=['S','K','T', 'sigma', 'r', 'n', 'option_type', 'Price'])

for K in american_tests:
    for option_type in ['call', 'put']:
        american = American(S, K,T, sigma, r, n, option_type)
        american_data.loc[len(american_data)-1]=[S,K,T,sigma,r,n,option_type,american.binomial_tree()]
american_data.to_csv('American_Tests.csv', index=False)

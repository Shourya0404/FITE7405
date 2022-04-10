from math import sqrt, log,exp,pi
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(2)
X=np.random.random((200))
np.random.seed(4)
Y=np.random.random((200))

X = X / np.linalg.norm(X)
Y = Y / np.linalg.norm(Y)

p=0.5
Z= X*p + sqrt(1-(p**2))*Y
print("Sample Size = 200")
print("\n")
print(f'Mean_X: {round(np.mean(X),2)} Mean_Y: {round(np.mean(Y),2)} Var_X: {round(np.var(X),2)} Var_Y: {round(np.var(Y),2)} Mean_Z: {round(np.mean(Z),2)} Var Z: {round(np.var(Z),2)}')
print("\n")
corr=np.cov(X,Z)[1,0]/(sqrt(np.var(X)*np.var(Z)))

print("The value of the correlation coefficient p(X,Z)= ",round(corr,2))
print("\n")
print(f"This value is slightly different from the theoretical value of 0.5. This is because the variables arent a perfect standard normal owing to the small sample size, X has a mean of {round(np.mean(X),2)} and a variance of {round(np.var(Y),2)}, while Y has a mean of {round(np.mean(X),2)} and a variance of {round(np.var(Y),2)}")

print("\n")
print("If the number of samples are increased, the distribution will be almost approximate to a standard normal and yield a correlation equal to the theoretical value of 0.5 (as seen below with a much larger sample size)")

np.random.seed(2)
X=np.random.random((20000000))
np.random.seed(4)
Y=np.random.random((20000000))
X = X / np.linalg.norm(X)
Y = Y / np.linalg.norm(Y)
p=0.5
Z= X*p + sqrt(1-(p**2))*Y
corr=np.cov(X,Z)[1,0]/(sqrt(np.var(X)*np.var(Z)))

print("\n")
print("Sample Size = 20000000")
print("\n")
print(f'Mean_X: {round(np.mean(X),2)} Mean_Y: {round(np.mean(Y),2)} Var_X: {round(np.var(X),2)} Var_Y: {round(np.var(Y),2)} Mean_Z: {round(np.mean(Z),2)} Var Z: {round(np.var(Z),2)}')
print("\n")
print("The value of the correlation coefficient p(X,Z)= ",round(corr,2))
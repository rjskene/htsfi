import numpy as np

from scipy.stats import invgauss, bernoulli as bern, norm, beta
from scipy.linalg import eigh, cholesky, svd
from ..main import *

# Loan amounts
n = 20
n_samples = 50000

loans_t = 2*10**6
randloans = np.random.uniform(0.1,1,n)
EAD = (randloans / randloans.sum())*loans_t
w = EAD / EAD.sum()

# PD for each borrower/loan.
pd_mu = 0.0044
pd_std = 0.002
p_of_d = np.random.normal(pd_mu, pd_std, n)
p_of_d = np.where(p_of_d<0, 0, p_of_d)
pd_var = bern.var(p_of_d)

# Correlation matrix
e = norm.rvs(0, 1, size=(n, n_samples)) # this creates defaults for ALL borrowers in ALL simulations
p = np.random.uniform(.01, .13, n)
corrmat = corrs_to_corrmat(p)

c = cholesky(corrmat, lower=True)

e_prime = np.dot(c, e).T
pd_inv = np.repeat(norm.ppf(p_of_d), n_samples).reshape(n_samples, n)

in_default = e_prime < pd_inv
default_per = (e_prime < pd_inv).sum() / (n*n_samples)

# LGD
mean = .4
lgd_std = .4
a, b = beta_params_from_descript(mean, lgd_std**2)
lgds = np.zeros(shape=in_default.shape) # LGDs for all loans start at 0%

i_loss = np.argwhere(in_default)
lgd_rands = beta.rvs(a, b, size=i_loss.shape[0]) 

# Insert LGDs where there was a default
for i in range(i_loss.shape[0]):
    x, y = i_loss[i]
    lgds[x, y] = lgd_rands[i]

losses = np.repeat(EAD, n_samples).reshape(n_samples, n) * lgds

simloss = losses.sum(axis=1)
simloss_gt0 = simloss[simloss>0]

params = beta.fit(simloss_gt0)
ld = beta(*params)

econ_cap = ld.ppf(0.9995)
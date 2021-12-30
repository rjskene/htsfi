import numpy as np

PD = np.around(
    np.array([
    0.03, 0.04, 0.04, 0.05, 0.08, 0.10, 0.13, 0.17, 0.24, 0.34, 
    0.53, 0.73, 1.40, 2.45, 6.00, 9.57, 16.72, 33.32
    ]) / 100,
5)
ODR = [10, 21, 24, 27, 31, 34, 37, 41, 44, 47, 51, 54, 57, 61, 64, 67, 70, 75, 80]
SP = np.array([
    'AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB',
    'BB-', 'B+', 'B', 'B-', 'CCC+', 'CCC-', 'CC'
])
SPRAT_KEY = {rat: p_of_d for rat, p_of_d in zip(SP, PD)}
PD_KEY = {v:k for k,v in SPRAT_KEY.items()}
PDMAP = {pd: {'odr': odr, 's&p': sp} for pd, odr, sp in zip(PD, ODR, SP)}

"""Distribution model for spread"""
from numpy.random import multivariate_normal
import numpy as np
import pandas as pd


def model(sl, size_l, size_r, N=3000,):
    """Model the spread based on price"""
    sl = sl.copy()
    sl['equity_l'] = size_l*sl['price_l']
    sl['equity_r'] = size_r*sl['price_r']

    cols = ['equity_l', 'equity_r']
    x = sl[cols]
    ds = multivariate_normal(x.mean().values, cov=np.cov(x.T.values), size=N)
    ds = pd.DataFrame(ds, columns=cols)
    ds['spread'] = (ds['equity_l'] - ds['equity_r'])
    d = ds['spread'].describe(percentiles=[0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])

    return d.to_dict()


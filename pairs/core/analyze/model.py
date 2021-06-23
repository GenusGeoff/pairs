"""Distribution model for spread"""
from numpy.random import multivariate_normal
import numpy as np
import pandas as pd


def model(sl, size_l, size_r, N=10000,):
    """Fit a multivariate normal model to prices and return description

    Returns summary statistics for the pair given by the dataframe `sl`
    and args `size_l` and `size_r`. Returns a dict like this one: 

    {'count': 3000.0, 'mean': -193.62872120093124, 'std':
    292.7382777219576, 'min': -1251.6540645297496, '1%':
    -871.9100156305747, '5%': -675.2979747087473, '10%':
    -575.1044231117638, '25%': -391.05357127026286, '50%':
    -191.46695115943157, '75%': -4.917967388586305, '90%':
    176.89984974160083, '95%': 299.0611286798856, '99%':
    522.6686244141971, 'max': 835.8231866947365}

    The value of the pair is calculated as:

        size_l*price_l - size_r-price_r

    A multivariate normal model is fit to the equity values of the price
    series (i.e. the quantity of shares times the price for either
    series) using `numpy.random.multivariate_normal`. Random samples are
    generated from this model and the descriptive stats of the pair are
    calculated. 

    Parameters
    ----------
    sl : DataFrame
        A dataframe of prices. Must have columns 'price_l' and
        'price_r'. 

    size_l, size_r : float
        The share size of each asset, i.e. the number of shares traded
        to trade the pair. 

    N : int
        The number of random variates to draw from in order to model the 
        spread. 

    Returns
    -------
    desc : dict
        A dict with descriptive statistics.

    """
    sl = sl.copy()
    sl['equity_l'] = size_l*sl['price_l']
    sl['equity_r'] = size_r*sl['price_r']

    cols = ['equity_l', 'equity_r']
    x = sl[cols]
    ds = multivariate_normal(x.mean().values, cov=np.cov(x.T.values), size=int(N))
    ds = pd.DataFrame(ds, columns=cols)
    ds['spread'] = (ds['equity_l'] - ds['equity_r'])
    percentiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
    d = ds['spread'].describe(percentiles=percentiles)

    return d.to_dict()

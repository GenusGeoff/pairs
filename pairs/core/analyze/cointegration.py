"""Analyze cointegration of two assets"""
from statsmodels.tsa.stattools import coint
import pandas as pd 


def is_cointegrated(df):
    """Returns True if price_l and price_r are cointegrated

    Parameters
    ----------
    df : DataFrame 
        Dataframe of prices. Must have columns 'date', 'price_l' and
        'price_r'. 

    Returns
    -------
    pass : bool
        If the p-value of the test is less than 0.01, the test has been
        passed and the value is True.

    """

    # create a dataframe of price returns
    sl = (df.sort_values(by=['date'])[['price_l', 'price_r']].copy()
            .pct_change().dropna(subset=['price_l']))

    # calculate the pvalue
    _, pvalue, _ = coint(sl['price_l'], sl['price_r'])

    return pvalue < 0.01

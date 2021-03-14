"""Funcs to retrieve data for a pair and setup"""
import pandas as pd
from ..yahoo_finance_data.retrieve import get_data


def get_pair(symbol_left, symbol_right):
    """Use yfinance to get daily data

    Returns a dataframe with columns date, price_l and price_r, i.e. 
    in this form: 

    | date                |   price_l |   price_r |
    |:--------------------|----------:|----------:|
    | 2021-03-08 00:00:00 |    255.31 |   2951.95 |
    | 2021-03-09 00:00:00 |    265.74 |   3062.85 |
    | 2021-03-10 00:00:00 |    264.9  |   3057.64 |
    | 2021-03-11 00:00:00 |    273.88 |   3113.59 |
    | 2021-03-12 00:00:00 |    268.4  |   3089.49 |

    """
    l = get_data(symbol_left, days=365*2).rename(columns={'close':'price_l'})
    r = get_data(symbol_right, days=365*2).rename(columns={'close':'price_r'})

    return l[['date', 'price_l']].merge(r[['date', 'price_r']], on=['date'])

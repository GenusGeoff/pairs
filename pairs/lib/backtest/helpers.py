"""Misc funcs for backtester"""
import pandas as pd
from io import StringIO
from . import fb_amzn


def load_example():
    """Load example input data"""
    df = pd.read_csv(StringIO(fb_amzn.data))
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize('US/Central')

    return df

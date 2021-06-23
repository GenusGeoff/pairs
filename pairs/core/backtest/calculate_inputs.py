"""Create signals and other data required for backtesting"""
import pandas as pd


def setup(df, params):
    """Calculate data series required for the backtest. 

    Takes as input a dataframe with columns `['date', 'price_l',
    'price_r']` and returns a dataframe with columns `['date',
    'price_l', 'price_r', 'return_l', 'price_change_l', 'std_l',
    'std_pcg_l', 'return_r', 'price_change_r', 'std_r', 'std_pcg_r',
    'corr_rolling', 'size_l', 'size_r', 'spread', 'spread_std',
    'spread_mean', 'band_upper', 'signal_sell', 'band_lower',
    'signal_buy']`. 

    The share size of each side of the spread is calculated in a
    volatility weighted manner. The share quantity for the "left" asset
    is set to 1, and the share quantity (fractional) of the "right"
    asset is:

        price_l*std_l / price_r*std_r

    ...where the price is the column "price_x" in `df` and the standard
    deviations "std_x" is an n-period rolling standard deviation, where
    "n" is specified in `params`. 

    The share quantities are calculated for every row, and this is used
    to calculate the value of the "spread" at every row. 

    A row is deemed to be a buy (sell) signal if the value of the spread
    is higher (lower) than the mean by a standard deviation factor. This
    multiplier is specified in `params`. 

    The rolling correlation is calculated here but (as of this writing)
    is not used anywhere in the codebase. A later enhancement may
    include analysis of the correlation. 

    Parameters
    ----------
    df : DataFrame 
        Dataframe of prices. Must have columns 'date', 'price_l' and
        'price_r'. 

    params : dict
        A dict with keys window_std, window_corr, and factor_std.
        window_std and window_corr are the lookback periods for the
        standard deviation and correlation calculations, measured in
        terms of the number of rows in `df`. factor_std is number of
        standard deviations above or below the mean to constitute a buy
        or sell signal. 

    Returns
    -------
    df : DataFrame
        The same dataframe as passed, with columns `['date', 'price_l',
        'price_r', 'return_l', 'price_change_l', 'std_l', 'std_pcg_l',
        'return_r', 'price_change_r', 'std_r', 'std_pcg_r',
        'corr_rolling', 'size_l', 'size_r', 'spread', 'spread_std',
        'spread_mean', 'band_upper', 'signal_sell', 'band_lower',
        'signal_buy']`.

    """
    for col in ['date', 'price_l', 'price_r']:
        msg = f"Must have column '{col}' in df"
        assert col in df.columns.tolist(), msg

    # calculate returns, standard deviations 
    df = df.sort_values(by=['date']).reset_index(drop=True)
    for col in ['price_l', 'price_r']:
        col_ret = col.replace('price', 'return')
        col_pcg = col.replace('price', 'price_change')
        col_std = col.replace('price', 'std')
        col_std_pcg = col.replace('price', 'std_pcg')
        df[col_ret] = df[col].pct_change()
        df[col_pcg] = df[col] - df[col].shift(1)
        df[col_std] = df[col_ret].rolling(params['window_std']).std()
        df[col_std_pcg] = df[col_pcg].rolling(params['window_std']).std()

    # rolling correlation
    d = (df[['return_l', 'return_r']].rolling(params['window_corr']).corr()
           .reset_index())
    df['corr_rolling'] = \
        d[d['level_1'] == 'return_l'].set_index('level_0')['return_r']

    # calculate share sizes 
    df['size_l'] = 1
    df['size_r'] = (df['price_l']*df['std_l']) / (df['price_r']*df['std_r'])

    # calculate spread 
    df['spread'] = df['price_l'] - df['size_r'] * df['price_r']
    df['spread_std'] = df['spread'].rolling(params['window_std']).std()
    df['spread_mean'] = df['spread'].rolling(params['window_std']).mean()

    # create bands and signals
    df['band_upper'] =  (df['spread_mean'].shift(1) \
                         + params['factor_std']*df['spread_std'].shift(1))
    df['signal_sell'] = df['spread'] > df['band_upper']
    df['band_lower'] = (df['spread_mean'].shift(1) \
                        - params['factor_std']*df['spread_std'].shift(1))
    df['signal_buy'] = df['spread'] < df['band_lower']

    return df.sort_values(by=['date']).reset_index(drop=True)

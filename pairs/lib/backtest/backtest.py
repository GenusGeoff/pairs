import pandas as pd
from .model import model
from .config import params_all
from . import helpers
from .get_data import get_pair
from . import describe


def setup(df, params):
    """Create base inputs"""

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
    d = df[['return_l', 'return_r']].rolling(params['window_corr']).corr().reset_index()
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


def backtest(df=pd.DataFrame(), symbols=(), verbose=False, params='base_daily',
             example=True):
    """Backtest pairs trade given by df"""
    params = params_all[params]

    # TODO - might want to build a real logger, this is just a quick hack 
    if verbose:
        log = lambda msg: print(f"{msg}")
    else:
        log = lambda x: x

    if len(df):
        df = df.copy()
        log('setting up dataframe..')
        df = setup(df, params)
        log('done')
    elif symbols:
        log('retrieving data...')
        df = get_pair(symbols[0], symbols[1])
        log(f"done, got {len(df):,.0f} records ranging from "
            f"{df['date'].min()} to {df['date'].max()}")
        log('setting up dataframe..')
        df = setup(df, params)
        log('done')
    elif example:
        log('setting up dataframe, using example data...')
        df = setup(helpers.load_example(), params)
        log('done')
    else:
        raise Exception('Must pass either a dataframe or tuple of symbols.')

    # start backtest loop
    positions = list()
    position = dict()

    for i in df.dropna(subset=['spread']).index:
        if not position:
            if df.loc[i, 'signal_sell'] or df.loc[i, 'signal_buy']:
                msg = (f"{'sell' if df.loc[i, 'signal_sell'] else 'buy'} signal "
                       f"found at '{df.loc[i, 'date']}'")
                log(msg)
                # initiate a position 
                position['date_entry'] = df.loc[i, 'date']
                position['stats_entry'] = df.loc[i].to_dict()
                position['side'] = 'sell' if df.loc[i, 'signal_sell'] else 'buy'
                position['price_entry_l'] = df.loc[i, 'price_l']
                position['price_entry_r'] = df.loc[i, 'price_r']
                position['size_l'] = df.loc[i, 'size_l']
                position['size_r'] = df.loc[i, 'size_r']
                position['std_l'] = df.loc[i, 'std_l']
                position['std_r'] = df.loc[i, 'std_r']
                position['min_loss'] = 0
                position['date_min_loss'] = df.loc[i, 'date']

                # model the spread using model module 
                mod = model(df.loc[i-params['window_std']:i],
                            position['size_l'], position['size_r'])
                # calculate profit target and stop loss in dollar amounts
                position['target_profit'] = \
                    params['factor_profit_std']*mod['std']
                position['target_loss'] = \
                    -params['factor_loss_size']*position['target_profit']
                log(f"target profit: '{position['target_profit']:.2f}'")
                log(f"target loss: '{params['factor_loss_size']*position['target_profit']:.2f}'")
                log(f"spread: '{df.loc[i, 'spread']}'")
                log(f"spread_mean: '{df.loc[i, 'spread_mean']}'")

        elif position:
            # update position 
            # calculate current pl 
            if position['side'] == 'sell':
                pl = position['size_l']*(position['price_entry_l'] - df.loc[i, 'price_l']) \
                    + position['size_r']*(df.loc[i, 'price_r'] - position['price_entry_r'])
                # exit if the spread is below the lower range
                exit_on_band = df.loc[i, 'spread'] \
                    < (df.shift(1).loc[i, 'spread_mean'] \
                       - params['factor_std']*df.shift(1).loc[i, 'spread_std'])
            elif position['side'] == 'buy':
                pl = position['size_l']*(df.loc[i, 'price_l'] - position['price_entry_l']) \
                    + position['size_r']*(position['price_entry_r'] - df.loc[i, 'price_r'])
                # exit if the spread is above the upper range
                exit_on_band = df.loc[i, 'spread'] \
                    > (df.shift(1).loc[i, 'spread_mean'] \
                       + params['factor_std']*df.shift(1).loc[i, 'spread_std'])

            # update max loss 
            # TODO - prob remove the max loss data later, remove from setup too 
            if pl < position['min_loss']:
                position['min_loss'] = pl
                position['date_min_loss'] = df.loc[i, 'date']

            # exit if profit threshold is reached, stop thresh. reached, or band reached
            exit_take_profit = pl >= position['target_profit']
            exit_stop_loss = pl <= position['target_loss']
            if exit_take_profit or exit_stop_loss or exit_on_band:
                msg = (f"position initiated on '{position['date_entry']}' "
                       f"has profit '{pl}', exiting position on bar "
                       f"'{df.loc[i, 'date']}'.")
                log(msg)
                msg = f"max loss: {position['min_loss']:.2f} @ {position['date_min_loss']}"
                log(msg)
                # exit position
                position['date_exit'] = df.loc[i, 'date']
                position['stats_exit'] = df.loc[i].to_dict()
                position['price_exit_l'] = df.loc[i, 'price_l']
                position['price_exit_r'] = df.loc[i, 'price_r']
                position['profit'] = pl
                if exit_take_profit:
                    position['exit_reason'] = 'take profit'
                elif exit_stop_loss:
                    position['exit_reason'] = 'stop loss'
                elif exit_on_band:
                    position['exit_reason'] = 'band exit'
                positions.append(position)
                position = dict()

    positions = pd.DataFrame(positions)
    stats = describe.create_stats(positions, params)
    table = describe.create_stats_table(df, positions, stats)

    return df, positions, stats, table

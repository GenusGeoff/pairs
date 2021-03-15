"""Funcs to analyze outcome of backtest"""
import pandas as pd
from tabulate import tabulate
from ..analyze.cointegration import is_cointegrated


def create_stats(df, positions, params):
    """Summarize outome of backtest"""
    stats = dict()
    stats['count_trades'] = len(positions)
    m = positions['profit'] < 0
    stats['count_losing_trades'] = len(positions[m])
    m = positions['profit'] >= 0
    stats['count_winning_trades'] = len(positions[m])
    assert stats['count_winning_trades'] + stats['count_losing_trades'] \
        == stats['count_trades']
    stats['winrate'] = stats['count_winning_trades'] / stats['count_trades']
    stats['profit_max'] = positions['profit'].max()
    stats['loss_max'] = positions['profit'].min()
    stats['sum_profit'] = positions['profit'].sum()
    stats['exit_reasons'] = (positions['exit_reason'].value_counts() \
                             / len(positions)).to_dict()
    stats['general_params'] = params
    stats['is_cointegrated'] = is_cointegrated(df)

    stats['profit_mean'] = \
        positions.loc[positions['profit'] >= 0, 'profit'].mean() 
    stats['loss_mean'] = \
        positions.loc[positions['profit'] < 0, 'profit'].mean() 

    # add share size 
    d = df.iloc[-1]
    stats['size_shares_left'] = d['size_l']
    stats['size_shares_right'] = d['size_r']
    # add share standard deviation 
    stats['std_left'] = d['std_pcg_l']
    stats['std_right'] = d['std_pcg_r']

    # calculate distance between rows 
    stats['barsize'] = (df['date'] - df['date'].shift(1)).dropna().median()

    return stats


def create_stats_table(df, positions, stats):
    """Create a display table of backtest history"""

    # list of metrics to include in order, along with text formatters 
    f = lambda x: x
    fi = lambda x: f"{x:,.0f}"
    ff = lambda x: f"{x:,.2f}"
    fp = lambda x: f"{100*x:.2f}%"
    fd = lambda x: f"${x:,.2f}"
    fdt = lambda x: f"{x.isoformat()}"
    metrics_formatters = [
        ('date_min', fdt), ('date_max', fdt), 
        ('param_factor_loss_size', ff), 
        ('param_factor_profit_std', ff), 
        ('param_factor_std', ff), 
        ('param_window_corr', fi), 
        ('param_window_std', fi), 
        ('count_data_points', fi),
        ('barsize', f),
        ('is_cointegrated', f),
        ('count_trades', fi), ('winrate', fp),
        #('count_losing_trades', fi), ('count_winning_trades', fi),
        ('profit_max', fd), ('loss_max', fd),
        ('sum_profit', fd), 
        ('profit_mean', fd), ('loss_mean', fd),
        ('size_shares_left', ff), ('size_shares_right', ff),
        ('std_left', fd), ('std_right', fd),
    ]

    tb = (pd.DataFrame.from_dict(stats, orient='index', columns=['value'])
            .reset_index().rename(columns={'index':'metric'})
            .reset_index(drop=True))

    # unpack params keys 
    for k,v in stats['general_params'].items():
        tb = tb.append({'metric':f"param_{k}", 'value':stats['general_params'][k]}, ignore_index=True)

    d = [
        {'metric':'date_min', 'value':df['date'].min()}, 
        {'metric':'date_max', 'value':df['date'].max()},
        {'metric':'count_data_points', 'value':len(df)},
    ]
    tb = tb.append(d, ignore_index=True)

    # set order  
    idx = [x[0] for x in metrics_formatters]
    tb = tb.set_index('metric').reindex(idx).reset_index()

    # apply formatters 
    for i in tb.index:
        f = dict(metrics_formatters)[tb.loc[i, 'metric']]
        tb.loc[i, 'value'] = f(tb.loc[i, 'value'])

    t = tabulate(tb, headers=tb.columns, tablefmt='pipe')

    return t

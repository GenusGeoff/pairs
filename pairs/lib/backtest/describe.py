"""Funcs to analyze outcome of backtest"""
import pandas as pd
from tabulate import tabulate


def create_stats(positions, params):
    """Summarize outome of backtest"""
    stats = dict()
    stats['count_trades'] = len(positions)
    m = positions['profit'] < 0
    stats['count_losing_trades'] = len(positions[m])
    m = positions['profit'] >= 0
    stats['count_winning_trades'] = len(positions[m])
    assert stats['count_winning_trades'] + stats['count_losing_trades'] == stats['count_trades']
    stats['winrate'] = stats['count_winning_trades'] / stats['count_trades']
    stats['profit_max'] = positions['profit'].max()
    stats['loss_max'] = positions['profit'].min()
    stats['sum_profit'] = positions['profit'].sum()
    stats['exit_reasons'] = (positions['exit_reason'].value_counts() / len(positions)).to_dict()
    stats['general_params'] = params

    stats['profit_mean'] = positions.loc[positions['profit'] >= 0, 'profit'].mean() 
    stats['loss_mean'] = positions.loc[positions['profit'] < 0, 'profit'].mean() 

    return stats


def create_stats_table(df, positions, stats):
    """Create a display table of backtest history"""

    # list of metrics to include in order, along with text formatters 
    fi = lambda x: f"{x:,.0f}"
    fp = lambda x: f"{100*x:.2f}%"
    fd = lambda x: f"${x:,.2f}"
    fdt = lambda x: f"{x.isoformat()}"
    metrics_formatters = [('count_trades', fi), ('count_losing_trades', fi),
               ('count_winning_trades', fi),
               ('winrate', fp), ('profit_max', fd), ('loss_max', fd),
               ('sum_profit', fd), ('profit_mean', fd),
               ('loss_mean', fd),]
    tb = (pd.DataFrame.from_dict(stats, orient='index', columns=['value'])
            .reset_index().rename(columns={'index':'metric'})
            .reset_index(drop=True))
    idx = [x[0] for x in metrics_formatters]
    tb = tb.set_index('metric').reindex(idx).reset_index()

    # apply formatters 
    for i in tb.index:
        f = dict(metrics_formatters)[tb.loc[i, 'metric']]
        tb.loc[i, 'value'] = f(tb.loc[i, 'value'])

    t = tabulate(tb, headers=tb.columns, tablefmt='pipe')

    return t

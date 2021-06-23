# A CLI for evaluating pairs trades

A CLI tool that backtests and analyzes trading pairs. A pair is a set of two assets, one of which is
purchased (long) and the other is sold (short). 

The backtesting logic included in this codebase was built under the assumption that the economic and
price relationship between the two assets is stable and has a tendency to revert to the mean,
especially when the price relationship is at an extreme. 

So, when the price of one asset in the pair is high relative to the other and to the historical
ratio, the pair is "sold", i.e. one asset is sold short and the other asset is bought long.
Alternatively, if the relative price is low, then the one asset is bought long and the other asset
is sold short. 

The `yfinance` ([link](https://github.com/ranaroussi/yfinance)) project is used to retrieve data for stocks. CLI functionality is handled by `cement`. 

The code that handles backtesting and data retrieval is in `pairs/core`. This is the location of all of the code that handles data 
retrieval/manipulation and backtesting. 

## Disclaimer

In no way, shape or form is `pairs` intended to be investment advice or a solicitation to engage in
any kind of financial transaction. While this codebase does summarize the past performance of
certain trading strategies, past performance is not indicative of future performance. The outcome of
these historical strategies can differ from actual trading for a large number of reasons, including
but not limited to: errors or inaccuracies in the `pairs` code; errors or inaccuracies in the
historical data used for generating the historical performance; changes in market dynamics;
transaction costs; or some other factor not listed here. Any individual or entity that chooses to
engage in any kind of financial transaction based on this codebase does so at their own risk. 

## Installation

There are at least two ways to utilize `pairs`. One is to install it directly via `pip`, the other
is to create a `virtualenv`.

If you wish, `pairs` can be installed directly with these two commands:

```
$ pip install -r requirements.txt

$ pip install setup.py
```

...and then you should be able to run `pairs --help` to get started. 

If you'd like instead to create a virtual environment, see the heading "Environment Setup" below.

## Usage

After installation, `pairs` can be used to backtest a pair of two stocks by running the below
command: 

```
pairs analyze-pair --symbols XLK,XLP
```

...where symbols "XLK" (tech ETF) and "XLP" (consumer staples ETF) are used as example symbols.
Nearly any pair of widely-traded stocks (or ETFs) should work. 

After running the above command, a table like the one below will be displayed: 

|    | metric                  | value               |
|---:|:------------------------|:--------------------|
|  0 | date_min                | 2019-03-18T00:00:00 |
|  1 | date_max                | 2021-03-12T00:00:00 |
|  2 | param_factor_loss_size  | 3.00                |
|  3 | param_factor_profit_std | 0.75                |
|  4 | param_factor_std        | 1.50                |
|  5 | param_window_corr       | 10                  |
|  6 | param_window_std        | 10                  |
|  7 | count_data_points       | 502                 |
|  8 | barsize                 | 1 days 00:00:00     |
|  9 | corr_last_10_bars       | 0.34                |
| 10 | corr_all                | 0.72                |
| 11 | is_cointegrated         | True                |
| 12 | count_trades            | 59                  |
| 13 | winrate                 | 74.58%              |
| 14 | profit_max              | $5.57               |
| 15 | loss_max                | $-5.66              |
| 16 | sum_profit              | $53.74              |
| 17 | profit_mean             | $1.90               |
| 18 | loss_mean               | $-2.00              |
| 19 | size_shares_left        | 1.00                |
| 20 | size_shares_right       | 5.34                |
| 21 | std_left                | $3.06               |
| 22 | std_right               | $0.56               |

TODO - create a table here that explains each of the rows in the above table. 

### Configuration 

`pairs` allows for custom user configuration via `PYaml`. To set up a custom configuration file, run
`pairs configure` where you will be presented with an interactive dialogue that sets up the
configuration file for you. 

The configuration file is broken up into sections. Here is the default configuration for the
`backtest_daily` section:

```
backtest_daily:
  factor_loss_size: 3
  factor_profit_std: 1.5
  factor_std: 2
  window_corr: 15
  window_std: 15
```

...configuration settings in this section are the paramaters for backtesting and analysis. Below is
an explanation of the parameters:

* `factor_loss_size` - the multiple of profit target for which to take a loss. 
* `factor_profit_std` - multiple of standard deviations of the pair to take a profit. 
* `factor_std` - multiple of standard deviation to define a sell or buy signal. 
* `window_corr` - lookback window for trailing correlation definition, number of price bars.
* `window_std` - lookback window for trailing mean/std for pair price, number of price bars.

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run pairs cli application

$ pairs --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Pairs`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it pairs --help
```

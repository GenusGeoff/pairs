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
The code that handles backtesting and data retrieval is in `pairs/lib`. 

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

After installation, `pairs` can be used to backtest a pair of two stocks like this: 

```
pairs analyze-pair --symbols SPY,QQQ
```

...where symbols "SPY" and "QQQ" are used as example symbols. Nearly any pair of widely-traded
stocks should work. Running `pairs analyze-pair` will result in a table in this form:

|    | metric            | value               |
|---:|:------------------|:--------------------|
|  0 | date_min          | 2019-03-14T00:00:00 |
|  1 | date_max          | 2021-03-12T00:00:00 |
|  2 | count_data_points | 504                 |
|  3 | count_trades      | 22                  |
|  4 | winrate           | 63.64%              |
|  5 | profit_max        | $10.76              |
|  6 | loss_max          | $-11.77             |
|  7 | sum_profit        | $28.71              |
|  8 | profit_mean       | $4.54               |
|  9 | loss_mean         | $-4.36              |

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

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

The `yfinance` project is used to retrieve data for stocks. CLI functionality is handled by `cement`.

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
pairs analyze-pair --symbols FB,AMZN
```

...where symbols "FB" and "AMZN" are used as example symbols. Nearly any pair of widely-traded
stocks should work. Running `pairs analyze-pair` will result in a table in this form:

|    | metric               | value                     |
|---:|:---------------------|:--------------------------|
|  0 | date_min             | 2019-03-14T00:00:00-05:00 |
|  1 | date_max             | 2021-03-12T00:00:00-06:00 |
|  2 | count_data_points    | 504                       |
|  3 | count_trades         | 21                        |
|  4 | winrate              | 52.38%                    |
|  5 | count_losing_trades  | 10                        |
|  6 | count_winning_trades | 11                        |
|  7 | profit_max           | $11.05                    |
|  8 | loss_max             | $-47.72                   |
|  9 | sum_profit           | $-170.58                  |
| 10 | profit_mean          | $6.82                     |
| 11 | loss_mean            | $-24.56                   |

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

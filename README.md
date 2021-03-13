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

The `yfinance` project is used to retrieve data for stocks. 


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

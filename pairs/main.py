
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import PairsError
from .controllers.base import Base
import os
from os.path import join, exists
from pathlib import Path

HOME = str(Path.home())

# configuration defaults
cfp = join(HOME, '.config', 'pairs')
if not exists(cfp):
    os.mkdir(cfp)
CONFIG = init_defaults('pairs', 'backtest_daily')
CONFIG['pairs']['config_filepath'] = join(cfp, 'pairs.yml')
CONFIG['backtest_daily']['window_std'] = 15
CONFIG['backtest_daily']['window_corr'] = 15
CONFIG['backtest_daily']['factor_std'] = 2
CONFIG['backtest_daily']['factor_profit_std'] = 1.5
CONFIG['backtest_daily']['factor_loss_size'] = 3


class Pairs(App):
    """Pairs primary application."""

    class Meta:
        label = 'pairs'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base
        ]


class PairsTest(TestApp,Pairs):
    """A sub-class of Pairs that is better suited for testing."""

    class Meta:
        label = 'pairs'


def main():
    with Pairs() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except PairsError as e:
            print('PairsError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()

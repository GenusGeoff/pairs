
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..core.backtest.backtest import backtest
from ..core.helpers import fmt_term
from os.path import join, exists
from textwrap import wrap
import yaml
from pathlib import Path
HOME = str(Path.home())

VERSION_BANNER = """
A CLI for evaluating pairs trades %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = ('A CLI for evaluating pairs trades. Run "pairs '
                       'analyze-pair" to display an example with archived '
                       'market data, or run "pairs analyze-pair -s '
                       '"TICKER1,TICKER2" to backtest/describe arbitrary tickers. ')
        description = '\n'.join(wrap(description, 80))

        # text displayed at the bottom of --help output
        epilog = 'Usage: pairs analyze-pair --symbols FB,AMZN'

        # controller level arguments. ex: 'pairs --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    @ex(help='Setup and modify app configuration settings.')
    def configure(self):
        """Setup app configuration"""
        cf = self.app.config
        p = lambda x: print(fmt_term(x))
        msg = (f"This dialogue sets up the configuration file for the pairs app. "
          f"")
        fp = cf.get('pairs', 'config_filepath')
        if exists(fp):
            msg += (f"Config file '{fp}' will be loaded and then overwritten. "
              f"Note that this file can be edited directly to change config "
              f"settings instead of using this dialogue. ")
        else:
            msg+= (f"A config file will be written to '{fp}', this file will "
              f"afterwards be referenced as the primary config file. "
              f"Note that after this initial setup '{fp}' can be edited directly to change config "
              f"settings (as opposed to using this dialogue). ")
        p(msg)
        p('')
        a = input(fmt_term("Press 'y' to accept all current settings or press "
                           "'enter' to review and optionally edit every "
                           "setting > "))
        if a != 'y':
            p('')
            p('Now each key present in the current config will be displayed and '
              'optionally changed. ')
            input('Press any key to continue...')
            p('')
            exclude = ['pairs', 'mail.dummy', 'log.colorlog', 'controller.base']
            for section in [x for x in cf.get_sections() if x not in exclude]:
                for key in cf.keys(section):
                    msg = (f"Config section '{section}' value '{key}' is currently "
                           f"set to '{cf.get(section, key)}'. ")
                    p(msg)
                    value = input(fmt_term("Press 'enter' to keep this value or input a "
                                           "different one > "))
                    if value:
                        cf.set(section, key, value)

        p('')
        with open(fp, 'w') as f:
            _ = yaml.dump(cf.get_dict(), f)
        p(f"Done, wrote (overwrote) config file to '{fp}'.")



    @ex(
        help='Backtest and describe a pair.',

        # sub-command level arguments. ex: 'pairs command1 --foo bar'
        arguments=[
            ( [ '-s', '--symbols' ],
             { 'help' : ('ticker symbols e.g. "FB,AMZN". If none passed, '
                         'then "FB,AMZN" will be used as an example.'),
                'action'  : 'store',
                'dest' : 'symbols' } ),
        ],
    )
    def analyze_pair(self):
        """Perform a backtest on a pair"""

        if self.app.pargs.symbols is not None:
            symbols = self.app.pargs.symbols.split(',')
            print(f"running backtest for {'-'.join(symbols)}:")
            df, positions, stats, table = \
                backtest(symbols=symbols)
            print(f"done, here are stats for {'-'.join(symbols)}:")
            print(table)
        else:
            print(f"running backtest for FB-AMZN using archived data:")
            df, positions, stats, table = backtest(example=True)
            print(f"done, here are stats for FB-AMZN:")
            print(table)

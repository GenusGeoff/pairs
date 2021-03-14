
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..core.backtest.backtest import backtest
from textwrap import wrap

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

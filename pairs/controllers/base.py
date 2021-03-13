
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..lib.backtest.backtest import backtest

VERSION_BANNER = """
A CLI for evaluating pairs trades %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'A CLI for evaluating pairs trades'

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
            print(f"running backtest for {data['symbol_left']}-{data['symbol_right']}:")
            df, positions, stats, table = \
                backtest(symbols=(data['symbol_left'], data['symbol_right']))
            print(f"done, here are stats for {data['symbol_left']}-{data['symbol_right']}:")
            print(table)
        else:
            print(f"running backtest for FB-AMZN using archived data:")
            df, positions, stats, table = backtest(example=True)
            print(f"done, here are stats for FB-AMZN:")
            print(table)

'''Usage: 
{0} initialize
{0} login
{0} (--help | --version)

Commands:
initialize  Create OR Reinitialize a configuration file to connect to Checkmarx cxsast v9.0

Report bugs to Uday Korlimarla <Uday.Korlimarla@checkmarx.com>
'''
import docopt
import sys
from pprint import pprint
from pathlib import Path
from .auth.auth import Auth
from .config import Config

__version__ = '0.0.1'

def main(sysargv=None):
    argv = docopt.docopt(
        doc=__doc__.format('cxacclient'),
        argv=sysargv,
        version=__version__
    )
    config = Config()
    config_checked = config.check_path()
    if argv['initialize']:
        if not config_checked:
    if argv['login']:
        pass


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

'''Usage:
{0} configtest 
{0} initialize
{0} (--help | --version)

Commands:
configtest  Verify configuration to connect to checkmarx cxsast v9.0
initialize  Create a configuration file to connect to Checkmarx cxsast v9.0

Report bugs to Uday Korlimarla <Uday.Korlimarla@checkmarx.com>
'''
import docopt
import sys

__version__ = '0.0.1'

def main(sysargv=None):
    argv = docopt.docopt(
        doc=__doc__.format('cxacclient'),
        argv=sysargv,
        version=__version__
    )
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

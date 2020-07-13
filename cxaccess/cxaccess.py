#!/usr/bin/env python3

'''Usage: 
{0} init [--verbose]
{0} login [--save] [--verbose]
{0} checktoken [--verbose]
{0} getroles [--save] [--verbose]
{0} updateroles [--verbose]
{0} getteams [--save] [--verbose]
{0} updateteams [--verbose]
{0} (-h | --help)
{0} version

Commands:
init            Create OR Reinitialize a configuration file to connect to Checkmarx cxsast v9.0
login           Authenticate user on Checkmarx
checktoken      Check token as unexpired. (Requires login --save to be used prior. )  
getroles        Fetch available roles locally
updateroles     Update LDAP Roles - Advanced Role Mapping. This replaces all existing roles
updateteams     Update LDAP Mappings to CxSAST Teams.

Options:
-s, --save               Save OAuth Token into configuration directory.
-h, --help               Help.
-v, --verbose            Display version of CxAccess.


Report bugs to Checkmarx (Cx TS-APAC) <TS-APAC-PS@checkmarx.com>
'''
import docopt
import sys
from pathlib import Path
from cxaccess.auth.auth import Auth
from cxaccess.config import Config
from cxaccess.teams.teams import Teams


__version__ = '0.0.11'

def main(sysargv=None):
    argv = docopt.docopt(
        doc=__doc__.format('cxaccess'),
        argv=sysargv,
        version=__version__
    )
    if argv['version']:
        print("CxAccess version: {0}".format(__version__))
        sys.exit(0)
    
    # Default to 
    verbose = False
    if argv['--verbose']:
        verbose = True

    config = Config(verbose)
    config_checked = None

    if argv['init']:
        if not config_checked:
            config_checked = config.check_path()
    
    # Perform Authentication and Save token
    if argv['login'] and argv['--save']:
        authy = Auth(verbose)
        authy.perform_auth(save_config=True)
    
    if argv['login'] and not argv['--save']:
        authy = Auth(verbose)
        authy.perform_auth()
    
    if argv['checktoken']:
        config.read_token()

    if argv['getteams']and argv['--save']:
        gt = Teams(verbose)
        gt.get_teams(save_config=True)
    
    # Can be optimized with the --save flag directly as boolean above
    if argv['getteams'] and not argv['--save']:
        gt = Teams(verbose)
        sys.stdout.flush()
        sys.stdout.write(str(gt.get_teams(save_config=False)))
    
    if argv['updateroles']:
        gt = Teams(verbose)
        gt.update_ac_roles()
    
    if argv['getroles'] and argv['--save']:
        gt = Teams(verbose)
        gt.save_ac_roles(save_config=True)

    # Can be optimized with the --save flag directly as boolean above
    if argv['getroles'] and not argv['--save']:
        gt = Teams(verbose)
        gt.save_ac_roles(save_config=False)
    
    if argv['updateteams']:
        gt = Teams(verbose)
        gt.update_teams()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    sys.exit(main(sys.argv[1:]))

'''Usage: 
{0} init
{0} login [-s]
{0} checktoken
{0} fetchteams [--suppress-members] [--suppress-ldap-groups] [-o] [-d] [-s]
{0} updateroles
{0} (-h | -ver)

Commands:
init            Create OR Reinitialize a configuration file to connect to Checkmarx cxsast v9.0
login           Authenticate user on Checkmarx
checktoken      Check token as unexpired. (Requires login --save )  
fetchteams      Fetch available teams locally
updateroles     Update LDAP Roles - Advanced Role Mapping

Options:
-s, --save                  Save OAuth Token into configuration directory.
-o, --stdout                STDOUT data for saving.
--suppress-members          Do not include Team's members data.
--suppress-ldap-groups      Do not include Team's LDAP Groupings (If multiple mappings are present).
-h, --help                  Help.
-ver, --version             Display version of CxAcClient.


Report bugs to Uday Korlimarla <Uday.Korlimarla@checkmarx.com>
'''
import docopt
import sys
from pprint import pprint
from pathlib import Path
from cxacclient.auth.auth import Auth
from cxacclient.config import Config
from cxacclient.teams.teams import Teams


__version__ = '0.0.1'

def main(sysargv=None):
    argv = docopt.docopt(
        doc=__doc__.format('cxacclient'),
        argv=sysargv,
        version=__version__
    )
    config = Config()
    config_checked = config.check_path()

    if argv['init']:
        if not config_checked:
            config_checked = config.check_path()
    
    # Perform Authentication and Save token
    if argv['login'] and config_checked and argv['--save']:
        authy = Auth()
        authy.perform_auth(save_config=True)
        

    if argv['login'] and config_checked and not argv['--save']:
        authy = Auth()
        authy.perform_auth()
    
    if argv['checktoken']:
        token_data = config.read_token()
        assert(token_data)
        print(u'\u2714', "Token is valid for use.")

    if argv['fetchteams']and argv['--save']:
        gt = Teams()
        gt.get_teams(save_config=True)
        print(u'\u2714', "Team Structure saved.")
    
    if argv['fetchteams']and argv['--stdout']:
        gt = Teams()
        sys.stdout.flush()
        sys.stdout.write(str(gt.get_teams()))
    
    if argv['updateroles']:
        gt = Teams()
        gt.update_ac_roles()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(sys.argv)
        sys.argv.append('-h')
    sys.exit(main(sys.argv[1:]))

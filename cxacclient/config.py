from pathlib import Path
import time
from os.path import exists as path_exists
from os.path import isdir
from os.path import isfile
from os import mkdir as create_directory
import yaml
from yaspin import yaspin
from cxacclient.utils.connections import Connection

# To-Do: De-duplicate read-write methods to a factory
# Reserving this for now as a future todo.

class Config(Connection):
    """
    Config depends on connection to make a predictable MRO only.
    However, MRO is being abused here to make connection available universally.
    """
    @yaspin(text="Checking Configuration", color="red")
    def __init__(self):
        super().__init__()
        self.config_path = Path.joinpath(Path().home(), ".cx")
        self.providers_config = self.config_path / "providers.yaml"
        self.team_config = self.config_path / "team.yaml"
        self.token_config = self.config_path / "token.yaml"
        self.cx_config = self.config_path / "cx.yaml"
        self.update_ldap_roles_config = self.config_path / "updateLdapRoles.yaml"
        self.read_update_teams_config = self.config_path / "updateTeams.yaml"
        self.ldap_provider_ids = list()
    
    def check_path(self):
        """
        Implicit check
        Touch and create yaml file in <user_home_dir>/.cx/ac.yaml
        Touch and create yaml file in <user_home_dir>/.cx/team.yaml
        """
        # To-Do: Loop over as the list has grown. Make this more pythonic.
        try:
            if not path_exists(self.config_path) or not isdir(self.config_path):
                print("Config Directory: {0}".format(self.config_path))
                create_directory(self.config_path)
            if not path_exists(self.providers_config) or not path_exists(self.team_config):
                print("creating Providers configuration at: {0}".format(self.providers_config))
                Path(self.providers_config).touch()

                print("creating Team configuration at: {0}".format(self.team_config))
                Path(self.team_config).touch()
            
            if not path_exists(self.token_config) or not path_exists(self.cx_config):
                print("creating Token config at: {0}".format(self.token_config))
                Path(self.token_config).touch()

                print("creating Cx config at: {0}".format(self.cx_config))
                Path(self.cx_config).touch()
            
            if not path_exists(self.read_update_teams_config) or not path_exists(self.update_ldap_roles_config):
                print("creating Update config at: {0}".format(self.read_update_teams_config))
                Path(self.read_update_teams_config).touch()

                print("creating Update config at: {0}".format(self.update_ldap_roles_config))
                Path(self.update_ldap_roles_config).touch()
            

            else:
                print("Configuration directory exists at: {0}".format(self.config_path))
            
            # Instead of the pythonic default None
            return True

        except Exception as err:
            # To-Do: Log this config creation exception
            print(err)
            print("Config files do no exist. Please run cxclient init OR cxclient login --save.")
            return

    # To-Do Get rid of these duplicated saves with a dict get config file path
    def save_cxconfig(self, meta):
        """
        Save CxServer config - SSL, Host
        """
        with open(self.cx_config, 'w') as cx_config_writer:
            print("Saving CxConfig at: {0}".format(self.cx_config))
            file_dump = yaml.dump(meta, cx_config_writer)
    
    def save_providers(self, meta):
        """
        Save Cx Auth Providers to providers.yaml
        """
        with open(self.providers_config, 'w') as provides_writer:
            print("Cx Auth providers: {0}".format(self.providers_config))
            file_dump = yaml.dump(meta, provides_writer)

    def save_token(self, meta):
        """
        Save OAuth Token to Configuration directory
        """
        # Check config directory exists
        self.check_path()
        # Always write mode to Update from Cx.
        with open(self.token_config, 'w') as token_writer:
            print("Token is at: {0}".format(self.token_config))
            file_dump = yaml.dump(meta, token_writer)
    
    def save_teams_config(self, meta):
        """
        Save teams to team_config.yaml
        """
        with open(self.team_config, 'w') as team_config_writer:
            print("Saving teams: {0}".format(self.team_config))
            file_dump = yaml.dump(meta, team_config_writer)

    def read_token(self):
        """
        Read token from config
        """
        self.check_path()
        try:
            with open(self.token_config, 'r') as token_reader:
                print("Reading token from disk: {0}".format(self.token_config))
                # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.

                data = yaml.full_load(token_reader)
                # Token is not expired 
                
                if data and int(data['exp']) - int(time.time()) > 0:
                    return data['token']
        except Exception as err:
            print("P")
            raise FileExistsError

    def read_cx_config(self):
        """
        Read CxConfig from config
        """
        with open(self.cx_config, 'r') as cx_config_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            print("Reading config from here: {0}".format(self.cx_config))
            return yaml.full_load(cx_config_reader)
    
    def read_providers_config(self):
        """
        Read Providers from config
        """
        with open(self.providers_config, 'r') as providers_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            print("Reading providers from disk: {0}".format(self.providers_config))
            return yaml.full_load(providers_reader)
    
    def read_update_ldap_config(self):
        """
        Read YAML for updating LDAP Roles
        for CxAC Advanced Roles Mapping
        """
        with open(self.update_ldap_roles_config, 'r') as update_ldap_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            print("Reading LDAP roles: {0}".format(self.update_ldap_roles_config))
            return yaml.full_load(update_ldap_reader)
    
    def write_update_ldap_config(self, meta):
        """
        Read YAML for updating LDAP Roles
        for CxAC Advanced Roles Mapping
        """
        with open(self.update_ldap_roles_config, 'w') as update_ldap_writer:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            print("Writing LDAP Config to: {0}".format(self.update_ldap_roles_config))
            file_dump = yaml.dump(meta, update_ldap_writer)

    def read_update_teams(self):
        """
        Read YAML to update teams
        """
        with open(self.read_update_teams_config, 'r') as read_update_teams:
            print("Reading: {0}".format(self.read_update_teams_config))
            return yaml.full_load(read_update_teams)

    def get_ldap_providers_config(self):
        """
        Get LDAP Providers from config file
        """
        providers = self.read_providers_config()
        # Get LDAP Provider IDs
        print("LDAP Provider IDs set")
        self.ldap_provider_ids = [provider['providerId'] for provider in providers if provider['providerType'] == 'LDAP']

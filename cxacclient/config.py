from pathlib import Path
import time
from os.path import exists as path_exists
from os.path import isdir
from os.path import isfile
from os import mkdir as create_directory
import yaml
import emoji
from cxacclient.utils.connections import Connection

class Config(Connection):
    def __init__(self):
        super().__init__()
        self.config_path = Path.joinpath(Path().home(), ".cx")
        self.providers_config = self.config_path / "providers.yaml"
        self.team_config = self.config_path / "team.yaml"
        self.token_config = self.config_path / "token.yaml"
        self.cx_config = self.config_path / "cx.yaml"
        self.update_ldap_roles_config = self.config_path / "updateLdapRoles.yaml"
        self.good = emoji.emojize(':thumbs_up:')
        self.ldap_provider_ids = list()
    
    def check_path(self):
        """
        Implicit check
        Touch and create yaml file in <user_home_dir>/.cx/ac.yaml
        Touch and create yaml file in <user_home_dir>/.cx/team.yaml
        """
        try:
            if not path_exists(self.config_path) or not isdir(self.config_path):
                print("{0} Config Directory: {1}".format(self.good, self.config_path))
                create_directory(self.config_path)
            if not path_exists(self.providers_config) or not path_exists(self.team_config) or not path_exists(self.token_config) or not path_exists(self.cx_config):
                print("{0} creating Providers configuration at: {1}".format(self.good, self.providers_config))
                Path(self.providers_config).touch()

                print("{0} creating Team configuration at: {1}".format(self.good, self.team_config))
                Path(self.team_config).touch()

                print("{0} creating Token config at: {1}".format(self.good, self.token_config))
                Path(self.token_config).touch()

                print("{0} creating Cx config at: {1}".format(self.good, self.cx_config))
                Path(self.cx_config).touch()
        
            return True

        except Exception as err:
            # To-Do: Log this config creation exception
            print(err)
            print("{0} => Directory configuration errors")
            return False

    # To-Do Get rid of these duplicated saves with a dict get config file path
    def save_cxconfig(self, meta):
        """
        Save CxServer config - SSL, Host
        """
        with open(self.cx_config, 'w') as cx_config_writer:
            file_dump = yaml.dump(meta, cx_config_writer)
    
    def save_providers(self, meta):
        """
        Save Cx Auth Providers to providers.yaml
        """
        with open(self.providers_config, 'w') as provides_writer:
            file_dump = yaml.dump(meta, provides_writer)

    def save_token(self, meta):
        """
        Save OAuth Token to Configuration directory
        """
        # Check config directory exists
        self.check_path()
        # Always write mode to Update from Cx.
        with open(self.token_config, 'w') as token_writer:
            file_dump = yaml.dump(meta, token_writer)
    
    def save_teams_config(self, meta):
        """
        Save teams to team_config.yaml
        """
        with open(self.team_config, 'w') as team_config_writer:
            print(self.team_config)
            file_dump = yaml.dump(meta, team_config_writer)

    def read_token(self):
        """
        Read token from config
        """
        # To-Do: Verify token data
        with open(self.token_config, 'r') as token_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            data = yaml.full_load(token_reader)
            # Token is not expired 

            if int(data['exp']) - int(time.time()) > 0:
                return data['token']

    def read_cx_config(self):
        """
        Read CxConfig from config
        """
        with open(self.cx_config, 'r') as cx_config_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            return yaml.full_load(cx_config_reader)
    
    def read_providers_config(self):
        """
        Read Providers from config
        """
        with open(self.providers_config, 'r') as providers_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            return yaml.full_load(providers_reader)
    def read_update_ldap_config(self):
        """
        Read YAML for updating LDAP Roles
        for CxAC Advanced Roles Mapping
        """
        with open(self.update_ldap_roles_config, 'r') as update_ldap_reader:
            # Do not use yaml.load - To avoid Arbitrary Code Execution through YAML.
            return yaml.full_load(update_ldap_reader)

    def get_ldap_providers_config(self):
        """
        Get LDAP Providers from config file
        """
        providers = self.read_providers_config()
        # Get LDAP Provider IDs
        self.ldap_provider_ids = [provider['providerId'] for provider in providers if provider['providerType'] == 'LDAP']

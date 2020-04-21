from pathlib import Path
from os.path import exists as path_exists
from os.path import isdir
from os.path import isfile
from os import mkdir as create_directory
import yaml
import emoji


class Config(object):
    def __init__(self):
        super().__init__()
        self.config_path = Path.joinpath(Path().home(), ".cx")
        self.ac_config = self.config_path / "ac.yaml"
        self.team_config = self.config_path / "team.yaml"
        self.good = emoji.emojize(':thumbs_up:')
    
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
            if not path_exists(self.ac_config) or not path_exists(self.team_config):
                print("{0} creating Login configuration at: {1}".format(self.good, self.ac_config))
                Path(self.ac_config).touch()
                print("{0} creating Team configuration at: {1}".format(self.good, self.team_config))
                Path(self.team_config).touch()

            else:
                print("{0} Config exists at: {1}".format(self.good, self.ac_config))
        
            return True

        except Exception as err:
            # To-Do: Log this config creation exception
            print("{0} => Directory configuration errors".format(self.cat))
            return False
    
    def login_conf(self):
        """
        Store Login conf without password
        """
        pass
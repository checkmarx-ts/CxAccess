from pathlib import Path
from pprint import pprint
from os.path import exists as path_exists
from os.path import isdir
from os.path import isfile
from os import mkdir as create_directory
import yaml


class Config(object):
    def __init__(self):
        super().__init__()
        self.config_path = Path.joinpath(Path().home(), ".cx")
        self.ac_config = self.config_path / "ac.yaml"
    
    def check_path(self):
        """
        Implicit check
        Touch and create yaml file in <user_home_dir>/.cx/ac.yaml
        """
        try:
            if not path_exists(self.config_path) or not isdir(self.config_path):
                pprint({"creating directory at:": self.config_path})
                create_directory(self.config_path)
            elif not path_exists(self.ac_config):
                pprint({"creating configuration at:": self.ac_config})
                Path(self.ac_config).touch()
            else:
                pprint({"Config location is set": str(self.ac_config)})
        
            return True
        except Exception as err:
            # To-Do: Log this config creation exception
            return False
    
    def login_conf(self):
        """
        Store Login conf without password
        """
        pass
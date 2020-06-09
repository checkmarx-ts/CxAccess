import urllib3
import requests

# This will help disable warnings in CLI
# Ideally this should be thrown
urllib3.disable_warnings()

class Connection(object):
    """
    Requets Session class
    """
    def __init__(self, verbose):
        super().__init__()
        self.verbose = verbose
        self.session = requests.Session()

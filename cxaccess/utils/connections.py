import urllib3
import requests
from yaspin import yaspin

# This will help disable warnings in CLI
# Ideally this should be thrown
urllib3.disable_warnings()

class Connection(object):
    """
    Requets Session class
    """
    @yaspin(text="connecting to CxAccessControl")
    def __init__(self, verbose):
        super().__init__()
        self.session = requests.Session()

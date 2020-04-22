import urllib3
import requests

urllib3.disable_warnings()

class Connection(object):
    """
    Requets Session
    """
    def __init__(self):
        super().__init__()
        self.session = requests.Session()

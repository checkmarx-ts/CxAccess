import urllib3
import requests
from PyInquirer import prompt
from auth import Auth

urllib3.disable_warnings()

class GetTeams(Auth):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    get_teams = GetTeams()
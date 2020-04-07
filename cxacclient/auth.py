import urllib3
import requests
from PyInquirer import prompt, Separator
from input_validators import PortValidator

# Dev Import
from pprint import pprint

urllib3.disable_warnings()

# To-DO: Assumption is SSL/TLS is enabled.
# HTTP Support to be enabled :facepalm:

class Auth(object):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.verify = True
        self.token = None
        self.host = "localhost"
        self.auth_payload = payload = 'username={0}&password={1}&grant_type=password&scope={2}&client_id={3}&client_secret=014DF517-39D1-4453-B7B3-9930C563627C'
        self.client_id = str()
        self.scope = str()
        self.auth_url = "https://{0}/cxrestapi/auth/identity/connect/token"

        self.headers = {
            'Accept': 'application/json;v=1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def set_host(self):
        """
        Set the URL Checkmarx CxSAST v9.0
        """
        host_questions = [
            {
                'type': 'input',
                'qmark': 'Checkmarx Host',
                'message': '(Default localhost).Checkmarx URL, IP, Host-Name or FQDN (Ex: uday.checkmarx.au):',
                'name': 'host',
                'default': 'uday.cx.au'
            },
            # To-DO support for HTTP
            # {
            #     'type': 'input',
            #     'qmark': 'Checkmarx Port',
            #     'message': 'Webserver port: Default is 443',
            #     'name': 'port',
            #     'default': '443',
            #     'validate': PortValidator
            # },

        ]
        host_answers = prompt(host_questions)
        self.auth_url = self.auth_url.format(host_answers['host'])
        self.host = host_answers
    
    def set_scope(self):
        scope_questions = [
            {
                'type': 'checkbox',
                'qmark': 'Login Scope',
                'message': 'Select login scope. Access Control is selected by default',
                'name': 'scope',
                'choices': [ 
                    Separator('*-* Select Login scope *-*'),
                    {
                        'name': 'sast_api'
                    },
                    {
                        'name': 'openid'
                    },
                    {
                        'name': 'sast-permissions'
                    },
                    {
                        'name' : 'access-control-permissions'
                    },
                    {
                        'name' : 'access_control_api',
                        'checked': True
                    }
                ]
            }
        ]
        scope_answers = prompt(scope_questions)
        pprint(scope_answers)
        self.scope = " ".join(scope_answers['scope'])
        pprint(self.scope)

    def check_ssl_verification(self):
        # Check SSL, If Self-Signed set SSL-Verify false with a prompt
        # To-DO: Promot this only if SSL Verify fails.
        ssl_questions = [
            {
                'type': 'confirm',
                'qmark': 'SSL Verification',
                'message': 'Turn off SSL Certificate verification',
                'name': 'sslVerify'
            }
        ]
        ssl_answer = prompt(ssl_questions)
        self.verify = not ssl_answer['sslVerify']
        pprint(ssl_answer)
    
    def set_client_id(self):
        # To-DO: Client Secret
        client_id_questions = [
            {
                'type': 'input',
                'qmark': 'CxREST API Client for use',
                'message': 'Default is resource_owner_client. Custom client use is to be implemented.',
                'name': 'client_id',
                'default': 'resource_owner_client'
            }
        ]
        client_id_answers = prompt(client_id_questions)
        print(client_id_answers)
        self.client_id = client_id_answers['client_id']
        pprint(self.client_id)
    
    @staticmethod
    def ask_creds():
        auth_questions = [
                            {
                                'type': 'input',
                                'qmark': 'Credentials',
                                'message': 'Checkmarx Username:',
                                'name': 'username',
                                'default': 'cx.au\\vader'
                            },
                            {
                                'type': 'password',
                                'message': 'Password:',
                                'name': 'password'
                            }
                        ]
        return prompt(auth_questions)

    def perform_auth(self):
        """
        Setting default scope to use just the AC Module
        """
        # Set Host, Scope and Client type
        self.set_host()
        self.set_scope()
        self.set_client_id()
        self.check_ssl_verification()
        creds = self.ask_creds()

        ###################
        # Do not log this #
        ###################
        payload = self.auth_payload.format(creds['username'], creds['password'], self.scope, self.client_id)
        
        try:
            response = self.session.request("POST", self.auth_url, headers=self.headers, data = payload, verify=self.verify)
        
            if response.ok:
                print(u'\u2714', " Authentication successfull.")
                self.token = "{0} {1}".format(response.json()['token_type'], response.json()['access_token'])
                print(self.token)
            else:
                print(u'\u274c', " Authentication unsuccessful.")
            
        except requests.exceptions.RequestException as http_err:
            # To-Do: Log error
            print(u'\u274c', " General Error occured.")
        
        creds = None
        

if __name__ == "__main__":
    auth = Auth()
    auth.perform_auth()
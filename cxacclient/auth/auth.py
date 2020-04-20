import urllib3
from json import loads
import requests
from PyInquirer import prompt, Separator
from .input_validators import PortValidator

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
        self.auth_provider = "Application"
        self.auth_payload = payload = 'username={0}&password={1}&grant_type=password&scope={2}&client_id={3}&client_secret=014DF517-39D1-4453-B7B3-9930C563627C'
        self.client_id = str()
        self.scope = str()
        self.base_url = "https://{0}/cxrestapi/auth{1}"

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
            #     'message': 'Webserver port: Default is 80',
            #     'name': 'port',
            #     'default': '80',
            #     'validate': PortValidator
            # },

        ]
        host_answers = prompt(host_questions)
        self.host = host_answers['host']
    
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
        self.scope = " ".join(scope_answers['scope'])

    def check_ssl_verification(self):
        # Check SSL, If Self-Signed set SSL-Verify false with a prompt
        try:
            url = self.base_url.format(self.host, "/AuthenticationProviders")
            self.session.get(url=url)
        except Exception as err:
            #To-DO: Log here
            pprint({u'\u274c SSL Error': " Turing off SSL Verification"})
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
        self.client_id = client_id_answers['client_id']
    
    def ask_domain(self):
        """
        Check available domains configured on Checkmarx Access Control Module
        """
        auth_providers_url = self.base_url.format(self.host, "/AuthenticationProviders")
        auth_providers_response = self.session.request('GET', url=auth_providers_url, verify=self.verify)

        auth_provider_questions = [
            {
                'type': 'checkbox',
                'qmark': 'Authentication Providers',
                'message': 'Select login scope. Access Control is selected by default',
                'name': 'provider',
                'choices': [ 
                    Separator('*-* Select Authentication proviers *-*'),
                ],
                'validate': lambda answer: 'You must choose one.' if not len(answer) == 1 else True
            }
        ]
        # Setting a static index here.
        for auth_provider in auth_providers_response.json():
            auth_provider_questions[0]['choices'].append({'name': auth_provider['name']})
        
        auth_provider_answers = prompt(auth_provider_questions)
        if len(auth_provider_answers['provider']) == 0:
            auth_provider_answers['provider'].append('Application')
        
        self.auth_provider = auth_provider_answers['provider'][0]
        pprint({u'\u2714 Using Auth Provider': self.auth_provider})

    def ask_creds(self):
        domain_append = 'uday'

        print(self.auth_provider)
        if self.auth_provider != 'Application':
            domain_append = "{0}\\".format(self.auth_provider)
        
        auth_questions = [
                            {
                                'type': 'input',
                                'qmark': 'Credentials',
                                'message': 'Checkmarx Username:',
                                'name': 'username',
                                'default': domain_append
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
        self.ask_domain()
        creds = self.ask_creds()
        print(creds)

        ###################
        # Do not log this #
        ###################
        payload = self.auth_payload.format(creds['username'], creds['password'], self.scope, self.client_id)
        auth_url = self.base_url.format(self.host, "/identity/connect/token")
        
        try:
            response = self.session.request("POST", auth_url, headers=self.headers, data = payload, verify=self.verify)
        
            if response.ok:
                pprint({u'\u2714 Authentication' : "successfull."})
                self.token = "{0} {1}".format(response.json()['token_type'], response.json()['access_token'])
            else:
                # To-DO: Log Error
                pprint({u'\u274c Authentication': "unsuccessful", "status_code": response.status_code})
            
        except requests.exceptions.RequestException as http_err:
            # To-Do: Log error
            pprint({u'\u274c': " General Error occured.", "status_code": response.status_code})
        
        creds = None

from PyInquirer import prompt
import yaml
from cxacclient.config import Config


class Teams(Config):
    def __init__(self):
        super().__init__()
        config = self.read_cx_config()
        self.token = "Bearer {0}".format(self.read_token())
        self.payload = {}
        self.host = config['host']
        self.verify = config['ssl_verify']
        self.auth_provider = config['auth_provider']
        self.headers = {'Authorization': self.token, 'Accept': 'application/json;v=1.0'}
        self.teams_url = "https://{0}/CxRestApi/auth/Teams".format(self.host)
        self.ldap_team_mappings_url = "https://{0}/CxRestApi/auth/LDAPTeamMappings?ldapServerId={1}"
        self.cxac_roles_url = "https://{0}/CxRestApi/auth/Roles".format(self.host)
        self.ldap_roles_mappings_url = "https://{0}/CxRestApi/auth/LDAPRoleMappings?ldapServerId={1}"
        self.ldap_team_mappings = list()
        self.ldap_role_mappings = list()
        self.get_ldap_team_mappings()
        self.cxac_roles = list()
        self.get_ac_roles()
        
    def get_teams(self, save_config=False):
        """
        Fetch all teams on CxAC
        """
        try:
            response = self.session.request("GET", self.teams_url, data=self.payload, headers=self.headers, verify=self.verify)
            if response.ok:
                # Trusting response.json implicitly
                teams_data = response.json()
                
                meta_teams_data = list()
                # Maybe i should not do list-comprehension here to keep it readable (Maybe not)
                for team in teams_data:
                    team['members'] = self.get_team_members(team_id=team['id'])
                    team['ldap_team_mappings'] = [x for x in self.ldap_team_mappings if x['teamId']==team['id']]
                    meta_teams_data.append(team)

                if save_config:
                    self.save_teams_config(meta=meta_teams_data)
                    print(u'\u2714', "Teams config fetch successfull.")
                    return True
                else:
                    return meta_teams_data
            else:
                print(u'\u274c', "Teams fetch unsuccessful")

        except Exception as err:
            # To-DO: Log err
            return

    def get_team_members(self, team_id):
        """
        Fetch Team Members for a team
        Note: Not LDAP Groups, only team members
        """
        team_users_url = "{0}/{1}/Users".format(self.teams_url, team_id)

        try:
            response = self.session.request("GET", team_users_url, data=self.payload, headers=self.headers, verify=self.verify)
            if response.ok:
                members_data = response.json()
                if members_data:
                    members = [ {"userName": member_data["userName"], "email": member_data["email"]} for member_data in members_data]
                    return members
                else:
                    return list()
            else:
                return
        except Exception as err:
            #To-DO: Log err
            return

    def get_ldap_team_mappings(self):
        """
        Get LDAP Mappings for teams
        """
        self.get_ldap_providers_config()

        for ldap_provider_id in self.ldap_provider_ids:
            ldap_url = self.ldap_team_mappings_url.format(self.host, ldap_provider_id)
            try:
                response = self.session.request('GET', ldap_url, data=self.payload, headers=self.headers, verify=self.verify)
                if response.ok:
                    self.ldap_team_mappings = response.json()

            except Exception as err:
                # To-Do: Log err
                raise Exception

    def get_ldap_role_mappings(self, ldapServerId):
        """
        Get LDAP Roles
        """
        url = self.ldap_roles_mappings_url.format(self.host, ldapServerId)
        print(url)
        try:
            response = self.session.request('GET', url=url, data=self.payload, headers=self.headers, verify=self.verify)
            if response.ok:
                self.ldap_role_mappings = response.json()
        except Exception as err:
            print(err)
            raise Exception
        

    def get_ac_roles(self):
        """
        Get All roles on Access Control
        """
        try:
            response = self.session.request('GET', self.cxac_roles_url, data=self.payload, headers=self.headers, verify=self.verify)
            if response.ok:
                self.cxac_roles = [{'id': role['id'], 'name': 'SAST Data Cleaner' }for role in response.json()]               
                    
        except Exception as err:
            # To-Do: Log err
            raise Exception

import json
from PyInquirer import prompt
import yaml
from yaspin import yaspin
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
        # Get All Roles on AC and LDAP Teams, Roles
        self.cxac_roles = list()
        self.ldap_team_mappings = list()
        self.ldap_role_mappings = list()
        self.get_ac_roles()
        self.get_ldap_team_mappings()
        
        self.get_ldap_role_mappings()
    
    def roles_team_helper(self, ldap_team_mappings):
        """
        Helper method to make code less ugly
        """
        roles = list()
        if ldap_team_mappings:
            ldap_dn_list = [x['ldapGroupDisplayName'] for x in ldap_team_mappings]
            roles = [x['role'] for x in self.ldap_role_mappings if x['ldapGroupDn'] in ldap_dn_list]
        return roles


    def get_teams(self, save_config=False):
        """
        Fetch all teams on CxAC
        """
        response = self.session.request("GET", self.teams_url, data=self.payload, headers=self.headers, verify=self.verify)
        if response.ok:
            # Trusting response.json implicitly
            teams_data = response.json()
            
            meta_teams_data = list()
            # Maybe i should not do list-comprehension here to keep it readable (Maybe not)
            for team in teams_data:
                team['members'] = self.get_team_members(team_id=team['id'])
                team['ldap_team_mappings'] = [x for x in self.ldap_team_mappings if x['teamId']==team['id']]
                team['roles'] = self.roles_team_helper(ldap_team_mappings=team['ldap_team_mappings'])
                
                meta_teams_data.append(team)

            if save_config:
                self.save_teams_config(meta=meta_teams_data)
                print(u'\u2714', "Teams config fetch successfull.")
                return True
            else:
                print("Not saving")
                return meta_teams_data
        else:
            print(u'\u274c', "Teams fetch unsuccessful")

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
                    self.ldap_team_mappings.extend(response.json())

            except Exception as err:
                # To-Do: Log err
                raise Exception

    def get_ldap_role_mappings(self):
        """
        Get LDAP Roles
        """
        for ldap_provider_id in self.ldap_provider_ids:
            url = self.ldap_roles_mappings_url.format(self.host, ldap_provider_id)
            try:
                response = self.session.request('GET', url=url, data=self.payload, headers=self.headers, verify=self.verify)
                if response.ok:
                    ldap_roles_data = response.json()
                    for ldap_role_d in ldap_roles_data:
                        x = {'role': self.get_role_name(ldap_role_d['roleId']), 'ldapGroupDn': ldap_role_d['ldapGroupDn'], 'ldapGroupDisplayName': ldap_role_d['ldapGroupDisplayName']}
                        self.ldap_role_mappings.append(x)

                else:
                    # To-Do: Log err
                    print(response.status_code, response.reason)
            except Exception as err:
                # To-Do: Log err
                raise Exception

    def get_ac_roles(self):
        """
        Get All roles on Access Control
        """
        try:
            response = self.session.request('GET', self.cxac_roles_url, headers=self.headers, verify=self.verify)

            if response.ok:
                self.cxac_roles = [{'id': role['id'], 'name': role['name'] }for role in response.json()]
            else:
                print(response.status_code, response.reason)
                print(response.json()['Message'])
                    
        except Exception as err:
            # To-Do: Log err
            raise Exception
    
    def get_role_name(self, roleId):
        """
        Get Role Name from roleID
        """
        role = [x for x in self.cxac_roles if x['id'] == roleId]
        if role:
            return role[0]['name']

    def get_role_id(self, role):
        id = [x['id'] for x in self.cxac_roles if x['name'] == role]
        if id:
            return id[0]
        return
    
    def get_team_id(self, team_name):
        headers = self.headers
        headers['Content-Type'] = 'application/json;v=1.0'
        url = "https://{0}/CxRestAPI/auth/Teams".format(self.host)

        response = self.session.request('GET', url=url, headers=headers, verify=self.verify)

        if response.ok:
            teams = response.json()
            teamid = [team['id'] for team in teams if team['name'].lower() == team_name.lower()]
            if teamid:
                return teamid[0]
        else:
            print(response.status_code, response.reason)

    @yaspin(text="Updating roles ", color="yellow")
    def update_ac_roles(self):
        """
        Update roles
        """
        ldap_role_updates = self.read_update_ldap_config()
        headers = self.headers
        headers['Content-Type'] = 'application/json;v=1.0'

        ###################################
        ### Change 1 to Dynamic values ###
        ##################################
        url = "https://{0}/CxRestApi/auth/LDAPServers/1/RoleMappings".format(self.host)

        config_roles = []

        for ldap_role_update in ldap_role_updates:
            config_roles.append({
                'roleId': self.get_role_id(ldap_role_update),
                'ldapGroupDn': ";".join(ldap_role_updates[ldap_role_update])
            })
        config_roles = json.dumps(config_roles)
        
        headers = self.headers
        headers['Content-Type'] = 'application/json;v=1.0'
        
        #########
        ## Remove Static LdapserverID
        #########
        url = "https://{0}/CxRestApi/auth/LDAPServers/1/RoleMappings".format(self.host)
        response = self.session.request('PUT', url=url, headers=headers, data=config_roles, verify=self.verify)
        if response.ok:
            print('\u2714', "Roles Update succeeded.")
        else:
            print(response.reason, response.status_code)
            print('\u274c',"Roles update failed.")

    def save_ac_roles(self):
        """
        GET AC Roles and save to config
        """
        headers = self.headers
        headers['Content-Type'] = 'application/json;v=1.0'
        url = "https://{0}/CxRestApi/auth/LDAPRoleMappings?ldapServerId=1".format(self.host)
        response = self.session.request('GET', url=url, headers=headers, data={}, verify=self.verify)
        
        config_roles = {}

        if response.ok:
            for role in response.json():
                config_roles.update({
                    self.get_role_name(role['roleId']): role['ldapGroupDn'].split(";")
                })
            self.write_update_ldap_config(config_roles)
            print('\u2714', "Roles save succeeded.")
        else:
            print(response.reason, response.status_code)
            print(response.text)
            print('\u274c',"Roles save failed.")

    def update_teams(self):
        """
        Add LDAP Group Mappings to Cx Teams
        """
        teams = self.read_update_teams()
        config_teams = []

        for team in teams:
            x = teams[team].split(";")
            config_teams.append({
                "teamId": self.get_team_id(team),
                "ldapGroupDn": x[1],
                "ldapGroupDisplayName": x[0]
            })
 
        config_teams = json.dumps(config_teams)
        headers = self.headers
        headers['Content-Type'] = 'application/json;v=1.0'
        
        #########
        ## Remove Static LdapserverID
        #########
        url = "https://{0}/CxRestApi/auth//LDAPServers/1/TeamMappings".format(self.host)
        response = self.session.request('PUT', url=url, headers=headers, data=config_teams, verify=self.verify)
        
        if response.ok:
            print('\u2714',"teams update succeeded.")
        else:
            print(response.reason, response.status_code)
            print('\u274c',"Roles update failed.")
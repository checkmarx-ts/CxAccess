import json
from PyInquirer import prompt
import yaml
from cxaccess.config import Config


class Teams(Config):
    """
    LDAP Advanced Role Mappings & Checkmarx Team LDAP Mappings
    """
    def __init__(self, verbose):
        super().__init__(verbose)
        config = self.read_cx_config()
        if not config:
            print("Please check configuration files")
            self.logger.error("Please check configuration files")
            raise NotImplemented
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
        self.logger.info("Teams module initialized")
    
    def roles_team_helper(self, ldap_team_mappings):
        """
        Helper method to make code less ugly
        """
        roles = list()
        if ldap_team_mappings:
            ldap_dn_list = [x['ldapGroupDisplayName'] for x in ldap_team_mappings]
            roles = [x['role'] for x in self.ldap_role_mappings if x['ldapGroupDn'] in ldap_dn_list]
        return roles

    def iterate_team_ldap_mappings(self, data):
        # For teams that do no have LDAP Mappings
        if data == [] or not data:
            return []
        # For teams that have existing LDAP mapping
        config_data = []
        for d in data:
            config_data.append({d['ldapGroupDisplayName']: d['ldapGroupDn']})
        return config_data
    
    def prepare_team_data_write_meta(self, data):
        meta_config = dict()
        for d in data:
            meta_config.update({d["name"]: self.iterate_team_ldap_mappings(data=d['ldap_team_mappings']) })
        return meta_config
    
    def get_teams(self, save_config):
        """
        Fetch all teams on CxAC
        """
        response = self.session.request("GET", self.teams_url, data=self.payload, headers=self.headers, verify=self.verify)
        self.logger.info("URL: {0}".format(self.teams_url))
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
                self.save_teams_config(meta=self.prepare_team_data_write_meta(meta_teams_data))
                print("Teams config fetch successfull.")
                return True
            else:
                return meta_teams_data
        else:
            print("Teams fetch unsuccessful")
            self.logger.error("error in fetching teams. Response: {0}".format(response.text))

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
            self.logger.error("Error. {0}".format(err))
            return

    def get_ldap_team_mappings(self):
        """
        Get LDAP Mappings for teams
        """
        self.get_ldap_providers_config()
        ldap_url = self.ldap_team_mappings_url.format(self.host, self.ldap_provider_id)
        try:
            response = self.session.request('GET', ldap_url, data=self.payload, headers=self.headers, verify=self.verify)
            if response.ok:
                data = response.json()
                self.ldap_team_mappings.extend(data)

        except Exception as err:
            self.logger.error("Error. {0}".format(err))
            raise Exception

    def get_ldap_role_mappings(self):
        """
        Get LDAP Roles
        """

        url = self.ldap_roles_mappings_url.format(self.host, self.ldap_provider_id)
        try:
            response = self.session.request('GET', url=url, data=self.payload, headers=self.headers, verify=self.verify)
            if response.ok:
                ldap_roles_data = response.json()
                for ldap_role_d in ldap_roles_data:
                    x = {'role': self.get_role_name(ldap_role_d['roleId']), 'ldapGroupDn': ldap_role_d['ldapGroupDn'], 'ldapGroupDisplayName': ldap_role_d['ldapGroupDisplayName']}
                    self.ldap_role_mappings.append(x)

            else:
                self.logger.error("Error. {0}".format(response.text))
                print(response.status_code, response.reason)
        except Exception as err:
            self.logger.error("Error. {0}".format(err))
            raise Exception

    def get_ac_roles(self):
        """
        Get All roles on Access Control
        """
        print("Fetching Checkmarx Roles")
        try:
            response = self.session.request('GET', self.cxac_roles_url, headers=self.headers, verify=self.verify)

            if response.ok:
                self.cxac_roles = [{'id': role['id'], 'name': role['name'] }for role in response.json()]
            else:
                print(response.status_code, response.reason)
                print(response.json())
                self.logger.error(response.text)     
        except Exception as err:
            self.logger.error("Error. {0}".format(err))
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
            if self.verbose:
                print("Fetching teams failed")
                print(response.text)
            print(response.status_code, response.reason)
            self.logger.error(response.text)

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
        url = "https://{0}/CxRestApi/auth/LDAPServers/{1}/RoleMappings".format(self.host, self.ldap_provider_id)

        config_roles = []

        # To use multi-group entry in one-shot
        # for ldap_role_update in ldap_role_updates:
        #     config_roles.append({
        #         'roleId': self.get_role_id(ldap_role_update),
        #         'ldapGroupDn': ";".join(ldap_role_updates[ldap_role_update])
        #     })

        for ldap_role_update in ldap_role_updates:
            for group in ldap_role_updates[ldap_role_update]:
                config_roles.append({
                    'roleId': self.get_role_id(ldap_role_update),
                    'ldapGroupDn': group
                })
    
        config_roles = json.dumps(config_roles)
        headers = self.headers
        headers['Content-Type'] = 'application/json-patch+json;v=1.0'

        url = "https://{0}/CxRestApi/auth/LDAPServers/{1}/RoleMappings".format(self.host, self.ldap_provider_id)
        response = self.session.request('PUT', url=url, headers=headers, data=config_roles, verify=self.verify)
        if response.ok:
            print("Roles Update succeeded.")
        else:
            print(response.reason, response.status_code)
            
            print("Roles update failed")
            self.logger.error(response.text)

    def save_ac_roles(self, save_config):
        """
        GET AC Roles and save to config
        """
        headers = self.headers
        headers['Content-Type'] = 'application/json;v=1.0'
        url = "https://{0}/CxRestApi/auth/LDAPRoleMappings?ldapServerId={1}".format(self.host, self.ldap_provider_id)
        response = self.session.request('GET', url=url, headers=headers, data={}, verify=self.verify)
        
        config_roles = {}
        uniq_roles = None
        
        if response.ok:
            roles = response.json()
            uniq_roles = list(set([self.get_role_name(d['roleId']) for d in roles]))
            
            for uniq_role in uniq_roles:
                config_roles.update({uniq_role: []})
            
            for role in roles:
                iter_role = self.get_role_name(role['roleId'])
                if iter_role in uniq_roles:
                    existingMapppings = config_roles[iter_role]
                    existingMapppings.append(role['ldapGroupDn'])
                    config_roles.update({iter_role: existingMapppings})
            
            self.write_update_ldap_config(config_roles)
            print("Roles save succeeded.")
            self.logger.info("Roles saved")
        else:
            print(response.reason, response.status_code)
            print(response.text)
            print("Roles save failed.")
            self.logger.error("Roles save failed")
            self.logger.error(response.text)

    def update_teams(self):
        """
        Update LDAP Group Mappings to Cx Teams
        """
        try:
            teams_update = self.read_update_teams()
            cx_teams = list(teams_update.keys())
            config_teams = []

            # Each team here is a checkmarx team
            # Get the Team ID 

            for team in cx_teams:
                teamId = self.get_team_id(team)
                
                if self.verbose and not teamId:
                    print("Error: Team {0} does not exist".format(team))
                
                
                for index, ldap_team_map in enumerate(teams_update[team]):
                    dnName = list(ldap_team_map.keys())[0]
                    config_teams.append({
                        "teamId": teamId,
                        "ldapGroupDisplayName": dnName,
                        "ldapGroupDn": teams_update[team][index][dnName]
                    })
            
            config_teams = json.dumps(config_teams)
            headers = self.headers
            headers['Content-Type'] = 'application/json;v=1.0'
            
            url = "https://{0}/CxRestApi/auth/LDAPServers/{1}/TeamMappings".format(self.host, self.ldap_provider_id)
            response = self.session.request('PUT', url=url, headers=headers, data=config_teams, verify=self.verify)
            
            if response.ok:
                print("teams update succeeded.")
            else:
                print(response.reason, response.status_code)
                print("Roles update failed.")
                self.logger.error(response.text)
        
        except Exception as err:
            if self.verbose:
                print(err)
            self.logger.error(err)
            print("Could not update teams")

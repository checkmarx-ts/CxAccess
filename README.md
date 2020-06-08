# CxAccess
Checkmarx Access Control Helper for:
1. Manage Complex Users-Teams-Roles Structure with ease via CLI.
2. Perform Access Control Administrative tasks via CLI.


## Purpose
CxAccess helps with access management on Checkmarx more easier.
1. You can assign multiple LDAP Groups to a Checkmarx team.

--- 

# Getting Started

## Wiki
- To get started, Please visit the [wiki](https://github.com/checkmarx-ts/CxAccess/wiki/home). 

- For `Installation instructions` Please Visit [this section](https://github.com/checkmarx-ts/CxAccess/wiki/Installation) in the Wiki.


## Note
- The feature `updateroles` uses yaml file to update roles on Checkmarx. The contents of the yaml file are the effective roles that are published to `checkmarx`.

- To Observer changes from `updateroles`, Navigate to Checkmarx Access Control at `https://<fqdn>/CxRestApi/auth` and authenticate. After you authenticate, Visit, LDAP Settings and find the changes under Advanced LDAP Roles mappping.
---

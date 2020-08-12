---

To use the latest version of CxAccess (v0.0.15 and Above), Ensure that your Checkmarx CxSAST Instance is upgraded to v9.0 with Hotfix 8.

---

# CxAccess
Checkmarx Access Control Helper for:
1. Manage Complex Users-Teams-Roles Structure with ease via CLI.
2. Perform Access Control Administrative tasks via CLI.
3. Automate (Either as a cron or as API) the process of roles assignment.


## Purpose
CxAccess helps with access management on Checkmarx more easier.
1. Assign multiple LDAP Groups to a Checkmarx team with `updateteams`
2. Assign a Checkmarx role to multiple LDAP Groups with `updateteams`.

--- 

# Getting Started

## Wiki
- To get started, Please visit the [wiki](https://github.com/checkmarx-ts/CxAccess/wiki/home). 

- For `Installation instructions` Please Visit [this section](https://github.com/checkmarx-ts/CxAccess/wiki/Installation) in the Wiki.


## Note
- The feature `updateroles` uses yaml file to update roles on Checkmarx. The contents of the yaml file are the effective roles that are published to `checkmarx`.

- To Observer changes from `updateroles`, Navigate to Checkmarx Access Control at `https://<fqdn>/CxRestApi/auth` and authenticate. After you authenticate, Visit, LDAP Settings and find the changes under Advanced LDAP Roles mappping.


## Docker
- At this stage, Dockerfile is for testing changes in code quickly.
- This Dockerfile can be extended to run `cxaccess` toolkit, However, care must be taken to provide the yaml files.
- Please consider `fakeroot` if you use this dockerfile beyond testing code changes.
- Build command `docker build -t cxaccess:0.0.8 path/to/dockerfile`.
- Run command `docker run -it cxaccess`.
---

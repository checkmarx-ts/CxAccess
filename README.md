# Checkmarx Access Control Client
Checkmarx Access Control Client for:
1. Manage Complex Users-Teams-Roles Structure with ease via CLI.
2. Perform Access Control Administrative tasks via CLI.
---

# Q&A for Access Token
[![asciicast](https://asciinema.org/a/Zh3FeT2npJXbOW0c1AkNhc7I9.svg)](https://asciinema.org/a/Zh3FeT2npJXbOW0c1AkNhc7I9)
---

# Virtualenv
The venv module provides support for creating lightweight “virtual environments” with their own site directories, optionally isolated from system site directories. Each virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories.
---

# Development Instructions.

- Add Directorty to Python export `PYTHONPATH="${PYTHONPATH}:/my/other/path"`
---

- Clone & Install package in development mode with `-e` flag (` pip install -e .` from the directory). The `-e` ensures that when you write a new module, it is available for use without reinstalling `CxAcClient` package.
---

# Relative imports and packaging

To avoid any relative package imports during development, It is best to stick with adding this directory path to `PYTHONPATH`.
---

## Mac/Linux
- add  `export PYTHONPATH=$PYTHONPATH:/Users/uday/CxAcClient` to `.zprofile OR .bashprofile`
---

## Windows:
- Assuing Python was installed with `Add Python 3.8 to PATH` checked. [See here](https://docs.python.org/3/_images/win_installer.png)
-- Navigate to `My Computer > Properties > Advanced System Settings > Environment Variables >`
- Edit `PYTHONPATH`(if not existing) under `system variables`.
- *Append* the repo local clone to the python path. Instance: `C:\Users\udayk\CxAcClient;`
---

## But why?

- Importing a module is much easier.
- Instance: `from cxacclient.auth.auth import Auth`
---

# Contributing to this project

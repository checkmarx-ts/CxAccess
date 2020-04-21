# Checkmarx Access Control Client

# Q&A for Access Token


# Virtualenv


# Development Instructions.

- Add Directorty to Python export `PYTHONPATH="${PYTHONPATH}:/my/other/path"`

- Clone & Install package in development mode with `-e` flag (` pip install -e .` from the directory). The `-e` ensures that when you write a new module, it is available for use without reinstalling `CxAcClient` package.

# Relative imports and packaging

To avoid any relative package imports during development, It is best to stick with adding this directory path to `PYTHONPATH`.

## Mac/Linux
- add  `export PYTHONPATH=$PYTHONPATH:/Users/uday/CxAcClient` to `.zprofile OR .bashprofile`

## Windows:
- Assuing Python was installed with `Add Python 3.8 to PATH` checked. [See here](https://docs.python.org/3/_images/win_installer.png)
-- Navigate to `My Computer > Properties > Advanced System Settings > Environment Variables >`
- Edit `PYTHONPATH`(if not existing) under `system variables`.
- *Append* the repo local clone to the python path. Instance: `C:\Users\udayk\CxAcClient;`

## But why?

- Importing a module is much easier.
- Instance: `from cxacclient.auth.auth import Auth`
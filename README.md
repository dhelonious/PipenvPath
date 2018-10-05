# PipenvPath

Automatically add pipenv virtual environment paths to the Sublime Text 3 environment.

[Pipenv](https://github.com/pypa/pipenv) is a wonderful packaging and dependency management tool for Python. However, while it manages virtual environments automatically, the name and thus the path of the venvs are random/hashed. One could add the venv path manually on a per-project basis using the [Environment Settings](https://packagecontrol.io/packages/Environment%20Settings) plugin, though, this is tedious.

PipenvPath will automatically add the venv path managed by Pipenv to the *PATH* variable of the current project, which is yielded by the `pipenv --venv` command. This should work out of the box without any configuration, assuming that the Pipenv executable path is already provided by the *PATH* variable. Otherwise, the location of the Pipenv executable can be specified in `Preferences.sublime-settings`. A typical setup might look like this:
```json
    "pipenv_path":
    {
        "linux": "$HOME/.local/bin/pipenv",
        "windows": "%HOMEPATH%\\AppData\\Roaming\\Python\\Python37\\Scripts\\pipenv.exe"
    }
```

**NOTE**: You can also use the `"osx"` key (see the [sublime.platform()](https://www.sublimetext.com/docs/3/api_reference.html#sublime) documentation).

## Installation
Clone this repository to your Sublime Text 3 **Packages** folder. You can find it by using the menu: Preferences > Browse Packages...

## Credits
Based on the [Environment Settings](https://bitbucket.org/daniele-niero/environmentsettings) plugin by Daniele Niero.
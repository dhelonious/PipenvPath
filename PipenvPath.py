import os
import subprocess
import sublime
import sublime_plugin

PLATFORM = sublime.platform()
PIPENV = "pipenv"

def console_print(msg):
    print("PipenvPath: {}".format(msg))

def add_to_path(PATH, path):
    if PLATFORM == "windows":
        return ";".join((path+"\\Scripts", PATH))
    else:
        return ":".join((path+"/bin", PATH))

def remove_from_path(PATH, path):
    if PLATFORM == "windows":
        return PATH.replace(path+"\\Scripts;", "")
    else:
        return PATH.replace(path+"/bin:", "")

def plugin_loaded():
    settings = sublime.load_settings("Preferences.sublime-settings")
    global PIPENV
    if settings.get("pipenv_path"):
        PIPENV = settings.get("pipenv_path").get(PLATFORM, PIPENV)
        PIPENV = os.path.expandvars(PIPENV)
    console_print("pipenv executable: {}".format(PIPENV))

class ProjectEnvironmentListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwds):
        super(ProjectEnvironmentListener, self).__init__(*args, **kwds)

        self.active_project = None
        self.active_venv = None

    def on_activated(self, view):
        if self.active_project == sublime.active_window().project_file_name():
            return
        else:
            self.active_project = sublime.active_window().project_file_name()
            if self.active_project:
                sublime.set_timeout_async(self.set_pipenv_venv, 0)

    def get_venv_path(self):
        get_venv = subprocess.Popen(
            " ".join([PIPENV, "--venv"]),
            cwd=os.path.dirname(self.active_project),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        venv, error = get_venv.communicate()
        if error:
            console_print(error.decode().strip())
            return None
        if venv:
            venv_path = os.path.expandvars(venv.decode().strip())
            return venv_path

    def set_pipenv_venv(self):
        venv_path = self.get_venv_path()
        if not venv_path:
            return

        PATH = os.environ["PATH"]
        if self.active_venv:
            if venv_path != self.active_venv:
                PATH = remove_from_path(PATH, self.active_venv)
            else:
                return

        console_print("venv found at {}".format(venv_path))
        self.active_venv = venv_path
        os.environ["PATH"] = add_to_path(PATH, venv_path)
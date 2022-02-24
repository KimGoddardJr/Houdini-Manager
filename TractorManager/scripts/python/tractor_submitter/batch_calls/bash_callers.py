import subprocess
import platform
import os
from .path_methods import PathMethods


class SourceScript:
    def __init__(self, cmd_file_name, hip_file, nodes):

        # pwd_file = args[0]
        self.cmd_file = cmd_file_name
        # these are the arguments fed to self.cmd_file
        self.hou_file = hip_file
        self.nodes = nodes

        print(self.nodes)

        dir_path = PathMethods.GetRealPath()
        self.cmd_file_path = os.path.join(dir_path, self.cmd_file)

    def CallIt(self):

        subprocess.call(
            [
                "/usr/bin/env",
                "bash",
                self.cmd_file_path,
                self.hou_file,
                self.nodes,
            ]
        )

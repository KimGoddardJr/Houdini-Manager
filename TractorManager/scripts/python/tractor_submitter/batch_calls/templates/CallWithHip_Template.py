import hou
from time import sleep
import platform
import sys
import os
import json
import subprocess
import tractor.api.query as tq


class Process:
    def __init__(self, nodes):
        self.nodes = nodes

    def RenderIt(self):
        try:
            for node in self.nodes:
                cur_node = hou.node(node)
                if cur_node.type().name() == "opengl":
                    cur_node.render()

        except Exception as e:
            print(e)
            print("Something crashed")

            self.KillJob()
            raise

    def GetJobId(self):

        """
        Extract job id from file
        """
        cur_path = os.path.dirname(os.path.realpath(__file__))
        cur_jid_file = [file for file in os.listdir(cur_path) if "jid" in file.name()]
        cur_jid_file_path = os.path.join(cur_path, cur_jid_file[0])
        open_jid = open(cur_jid_file_path)

        jid_data = json.load(open_jid)

        jid = jid_data["jid"]

        return jid

    def KillJob(self):

        setup_tq_ownership = tq.setEngineClientParam(
            hostname="10.180.128.5", port=8080, user="root", debug=True
        )

        cur_task = tq.tasks(
            "jid={} and tid=1".format(self.GetJobId()), columns=["Job.owner"]
        )
        tq.skip(cur_task)
        tq.kill(cur_task)
        sleep(5)

    def EndJobSuccessfully(self):

        pass


if __name__ == "__main__":

    template_nodes = []

    render_gl = Process(template_nodes)
    render_gl.RenderIt()

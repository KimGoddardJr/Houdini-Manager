import hou
import os
import sys
import platform

from .bash_callers import SourceScript


class HythonCalls:
    def __init__(self, file):
        ### class vars ###
        self.hip_file = file
        hou.hipFile.load(self.hip_file)
        self.ogl_nodes = []

    def ProcessNodeTypes(self, node_list):
        # for node in nodes:
        node = str(node_list[0])
        print(node)
        get_node = hou.node(node)
        try:
            if get_node.type().name() == "topnet":
                self.ExecuteTop(node)
            elif get_node.type().name() == "ifd" or get_node.type().name() == "arnold":
                self.BruteRender(node)
            elif get_node.type().name() == "opengl":
                self.RenderOpenGL(node)
        except Exception as e:
            print(e)
            raise

        if len(self.ogl_nodes) >= 1:
            try:
                self.RenderOpenGL()
            except Exception as e:
                print(e)
                raise

    def BruteRender(self, node):
        print("rendering {}".format(node))
        get_node = hou.node(node)
        get_node.render()

    def ExecuteTop(self, path):
        """
        First cook the tops
        """
        path.executeGraph(False, True, False, False)

        """
        As soon as this is done, send the information to the database of the project.
        Have the project script refresh itself regularly.

        ****NICE EXTRA****
        Add a progress indicator to the Node being processed.
        """

    def RenderTops(self, path):

        # if self.ExecuteTop(path):
        """
        Check the folders for renderable files.
        initiate a RenderJob.
        depending on the context vary the RenderJob

        """
        pass

    def CheckTopOutputFolder(self):
        pass

    def QueryOpenGL(self, node):
        self.ogl_nodes.append(node)

    def RenderOpenGL(self, node):
        houdini_activator = os.path.join("activators", "activate_houdini_terminal.sh")
        ogl_render = SourceScript(houdini_activator, self.hip_file, node)
        ogl_render.CallIt()


class RenderJob:
    def __init__(self, file_type_path):
        self.file_type_path = file_type_path

    def CreateAlfjob(self):

        """
        Create different alf jobs depending on the context

        """

        pass

    def StartRender(self):
        pass


if __name__ == "__main__":

    hip_file = sys.argv[1]
    nodes = sys.argv[2:]

    print(nodes)
    setup_project = HythonCalls(hip_file)
    setup_project.ProcessNodeTypes(nodes)

    print(sys.argv)

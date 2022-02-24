import hou
from .hslu_gui_methods import DrawingMethods


class TrollMethods:

    ### Display troll image if sth is off ###
    @staticmethod
    def DrawMainFrame(nodes, widget_box, tractor_image, ugly_tractor):

        if (
            nodes.SelectedRenderNodes()
            or nodes.SelectedRopNodes()
            or nodes.AllRenderableNodes()
        ):
            widget_box.addLayout(DrawingMethods.DrawImage(tractor_image))
        else:
            widget_box.addLayout(DrawingMethods.DrawImage(ugly_tractor))

        return widget_box


class HoudiniPong:
    def __init__():
        pass

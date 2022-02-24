import hou
from PySide2 import QtCore
from .main_gui import MainWindow


###Call this function in Houdini XML configuration###
def go():
    # panetab = hou.ui.findPaneTab("panetab1")
    # panel = panetab.pane().floatingPanel()
    dialog = MainWindow()

    dialog.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
    # dialog.setParent(hou.qt.floatingPanelWindow(panel), QtCore.Qt.Window)
    dialog.show()

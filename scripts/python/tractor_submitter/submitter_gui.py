import datetime
from time import gmtime, strftime, sleep
import subprocess
import sys
import os
import errno
import re
import shutil
import math

from . submitter import TrHttpRPC, Spool, trAbsPath, jobSpool

import hou
from hutil.Qt import QtGui, QtWidgets, QtCore

'''

# reload this script in houdini with:

import tractor_submitter
reload(tractor_submitter.submitter_gui)

'''

## ------------------------------------------------------------- ##
sys.path.insert(1, os.path.join(sys.path[0], "blade-modules"))
## ------------------------------------------------------------- ##

# Creates the dialog box
class ExportDialog(QtWidgets.QWidget):

    finished = QtCore.Signal()

    def __init__(self, parent=None):
        super(ExportDialog, self).__init__()
        #self.parent = parent
        #resolution = ScreenInfo.resolution()
        self.initUI()

    def initUI(self):
        # size definitions
        resolution = QtWidgets.QApplication.desktop().availableGeometry()
        main_W = resolution.width() / 4
        main_H = resolution.height() / 2

        unit = resolution.width()/1920
        checkbox_constant = float(resolution.width())/160
        stylesheet = hou.qt.styleSheet()
        checkbox_stylesheet = "QListWidget::indicator {0} width: {1}px; height: {1}px;{2}".format("{",checkbox_constant,"}")

        self.setMinimumWidth(main_W)
        self.setMinimumHeight(main_H)

        self.setWindowTitle('Export to Tractor')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        #create a style guide for the layout colors
        self.setStyleSheet(stylesheet)

        # The main layout for the window
        main_layout = QtWidgets.QVBoxLayout()
        
        ################Draw an Image################
        cur_dir = os.path.dirname(__file__)
        #ugly_tractor = '{}/../../../config/Icons/ugly_tractor.jpg'.format(cur_dir)
        tractor_image = '{}/../../../config/Icons/TractorRenderSpool.png'.format(cur_dir)
        #if len(all_renderable_nodes()) <= 0:
        #    main_layout.addLayout(self.draw_image(ugly_tractor))
        #else:
        main_layout.addLayout(self.draw_image(tractor_image))
        #############################################
        self.setLayout(main_layout)
        main_layout.addStretch()

        ##### TRACTOR VARIABLES ######
        
        ##private variables
        self.tractorEngineName = '10.180.128.13'
        self.tractorEnginePort = 8080
        
        if 'TRACTOR_ENGINE' in os.environ.keys():
            name = os.environ['TRACTOR_ENGINE']
            self.tractorEngineName,n,p = name.partition( ":" )
            if p:
                self.tractorEnginePort = int( p )
        
        ##public variables
        main_layout.addStretch()
        #line input widgets from input fields
        input_fields = {"Crews","Tags","Envkey"}
        input_of_fields = []

        for field in input_fields:
            self.field = QtWidgets.QLineEdit()
            input_of_fields.append(self.field)
            #self.field.setStyleSheet(widget_stylesheet)
            self.field.setFixedSize((main_W*0.825),(main_H / 25))
            field_layout = QtWidgets.QHBoxLayout()
            field_layout.addWidget(QtWidgets.QLabel("{}:".format(field)))
            field_layout.addWidget(self.field)
            field_layout.setAlignment(QtCore.Qt.AlignCenter)
            #field_layout.addStretch()
            main_layout.addLayout(field_layout)

        zipObj = zip(input_fields,input_of_fields)
        self.dict_of_fields = dict(zipObj)

        main_layout.addStretch()
        # Priority and Start Time
        # Priority
        self.priority = QtWidgets.QComboBox()
        #self.priority.setStyleSheet(widget_stylesheet)

        priority_opt = ['Very Low', 'Low', 'Medium', 'High', 'Very High', 'Critical']
        for opt in priority_opt:
            self.priority.addItem(opt)
        self.priority.setCurrentIndex(2)
        # Begin time
        self.delay = QtWidgets.QComboBox()
        #self.delay.setStyleSheet(widget_stylesheet)

        delay_opts = ['Immediate', 'Manual', 'Delayed']
        for opt in delay_opts:
            self.delay.addItem(opt)
        self.delay.currentIndexChanged.connect(self.delaytime)

        #Hardware Spool
        self.blades = QtWidgets.QComboBox()
        #self.blades.setStyleSheet(widget_stylesheet)
        blade_opts = ['All GPUs', 'D300 GPUs', 'D500 GPUs', 'Linux']

        for opt in blade_opts:
            self.blades.addItem(opt)
        self.blades.setCurrentIndex(0)
        # Combo box options layout
        opts_layout = QtWidgets.QHBoxLayout()
        opts_layout.addWidget(QtWidgets.QLabel('Priority:'))
        opts_layout.addWidget(self.priority)
        #opts_layout.addWidget(QtWidgets.QLabel('Begin:'))
        #opts_layout.addWidget(self.delay)
        opts_layout.addWidget(QtWidgets.QLabel('Blade:'))
        opts_layout.addWidget(self.blades)
        #Frames per Unit Spinbox
        opts_layout.addWidget(QtWidgets.QLabel("Frames per Unit:"))
        self.fpu_spin = QtWidgets.QSpinBox()
        self.fpu_spin.setMinimum(1)
        self.fpu_spin.setFixedSize((main_W / 10),(main_H / 15))
        opts_layout.addWidget(self.fpu_spin)
        #opts_layout.addStretch()
        opts_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addLayout(opts_layout)

        main_layout.addStretch()

        self.boxcontainer = QtWidgets.QHBoxLayout()
        self.container_nodes = QtWidgets.QVBoxLayout()
        #self.container_checks = QtWidgets.QVBoxLayout()
        self.container_info = QtWidgets.QVBoxLayout()
        # Render Nodes Selection list
        self.select = QtWidgets.QListWidget()
        #self.checker = QtWidgets.QListWidget()
        self.select.setStyleSheet(checkbox_stylesheet)
        self.info = QtWidgets.QListWidget()
        self.select.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        #self.checker.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.info.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        def selection_type(nodelist_type):
            if len(nodelist_type) > 0:
                for node in nodelist_type:
                    rendernode = QtWidgets.QListWidgetItem(node.path())
                    rn_check = QtWidgets.QListWidgetItem("")
                    self.select.addItem(rendernode)
                    #self.checker.addItem(rn_check)
                    #if node.type().name() == "ifd":
                        #rendernode.setFlags(rendernode.flags() | QtCore.Qt.ItemIsUserCheckable)
                        #rendernode.setCheckState(QtCore.Qt.Unchecked)
                        #rendernode.setText("exportable as ifd".format(node.name()))
                    # must come after adding to widget
                    rendernode.setSelected(False)

                self.container_nodes.addWidget(QtWidgets.QLabel("Render Nodes"))
                self.container_nodes.addWidget(self.select)
                self.container_info.addWidget(QtWidgets.QLabel("Sent to Tractor"))
                self.container_info.addWidget(self.info)
                self.boxcontainer.addLayout(self.container_nodes)
                self.boxcontainer.addLayout(self.container_info)
                main_layout.addLayout(self.boxcontainer)

            else:
                info_layout = QtWidgets.QHBoxLayout()
                info_layout.addWidget(QtWidgets.QLabel('No renderable node found'))
                main_layout.addLayout(info_layout)

            return nodelist_type

        self.active_sel = []

        if selectedRenderNodes():
            selection_type(selectedRenderNodes())
            for node in selectedRenderNodes():
                self.active_sel.append(node)
        elif selectedRopNodes():
            selection_type(selectedRopNodes())
            for node in selectedRopNodes():
                self.active_sel.append(node)
        elif len(selectedRenderNodes()) < 1 or len(selectedRopNodes()) < 1:
            selection_type(all_renderable_nodes())
            for node in all_renderable_nodes():
                self.active_sel.append(node)

        # Buttons
        self.submit_btn = QtWidgets.QPushButton("Submit")
        self.submit_btn.clicked.connect(self.spoolJob)

        self.cancel_btn = QtWidgets.QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.close)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.submit_btn)

        main_layout.addLayout(btn_layout)


    def now(self):
        # Returns preformated time for now.
        return strftime("%H%M%S", gmtime())

    # Show/Hide the delay-time options
    def delaytime(self, index):
        i = 0
        items = self.delay_layout.count()
        while i<items:
            item = self.delay_layout.itemAt(i).widget()
            if item:
                item.setVisible(index == 2)
            i = i+1
    
    #update call functions
    def add_to_list(self,sent_node):
        self.info.addItem(sent_node)
    
    def export_file(self,node_parm):
        False
        node_parm.pressButton()
        return True
    
    def draw_image(self,image_pic):
        labelImage = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(image_pic)
        pixmap_small = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        labelImage.setPixmap(pixmap_small)
        pic_layout = QtWidgets.QHBoxLayout()
        pic_layout.addWidget(labelImage)
        pic_layout.setAlignment(QtCore.Qt.AlignCenter)
        return pic_layout

    #debug functions
    def makedir(self,folder_name):
        try:
            os.makedirs(folder_name)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass

    #--------------------------#
    #      TRACTOR METHODS     #
    #--------------------------#

    def spoolJob(self):
        #self.updateVariables()

        self.tractorEngine = '' + str( self.tractorEngineName ) + ':' + str( self.tractorEnginePort )

        for index, node in  enumerate(self.active_sel):

            cur_item = self.select.item(index)
            
            if cur_item.isSelected():
        
                jobScript = self.createJobScript(node)
                args = []
                args.append('--engine=' + self.tractorEngine)
                #if self.doJobPause:
                #    args.append('--paused')
                args.append(jobScript)

                Spool(args)

                sent_info = "{} submitted to Tractor".format(node.name())
                sent_node = QtWidgets.QListWidgetItem(sent_info)
                self.add_to_list(sent_node)

    def createJobScript(self, node):

        # Dispatch the job to tractor.
        # Spool out the houdini file.
        
        #spooledfiles = []
        
        hou_dir = hou.hipFile.path()
        spooldirname = os.path.dirname(hou_dir)
        
        hipfile_path = hou.hipFile.path()
        basefilename = os.path.basename(os.path.splitext(hipfile_path)[0])

        envkey = "TOOLS={} {}".format(os.environ.get('TOOLS'), self.dict_of_fields["Envkey"].text())

        if self.blades.currentText() == 'D300 GPUs':
            service = 'HoudiniRenderD300'
        elif self.blades.currentText() == 'D500 GPUs':
            service = 'HoudiniRenderD500'
        elif self.blades.currentText() == 'Linux':
            service = 'Linux'
        else:
            service = 'HoudiniRender'

        fpu = self.fpu_spin.value()


        #Create the .alf script to write on
        jobshort = "{}_{}_{}.alf".format(basefilename, node.name(), self.now())
        jobfull = os.path.join(spooldirname, jobshort)
        
        #start writing into .alf
        self.file = open(jobfull, 'w')
        #spooledfiles.append(jobfull)
        self.file.write("Job -title {{{}}}".format(jobshort))

        self.file.write(" -priority {}".format(self.priority.currentText()))
        self.file.write(" -tags {{ Houdini {} }}".format(self.dict_of_fields["Tags"].text()))

        self.file.write(" -service {{ {} }}".format(service))
        self.file.write(" -crews {{{}}}".format(self.dict_of_fields["Crews"].text()))

        self.file.write(" -projects Default")
        self.file.write(" -envkey {{{}}}".format(envkey))
        self.file.write(" -serialsubtasks 1")

        self.file.write(" -subtasks {\n")

        self.file.write("    Task {Render Frames} -subtasks {\n")

        #node range setting
        validFrameRange = node.parm('trange').eval()

        if validFrameRange == 0:
            node_start = int(hou.frame())
            node_end = int(hou.frame())
            node_step = 1
        else:
            node_start = int(node.parm('f1').eval())
            node_end = int(node.parm('f2').eval())
            node_step = int(node.parm('f3').eval())

        #start standard hqueue render

        #def export_mode(self,node,cachefile_extension):
        #relative path for file export in houdini

        node_type_name = node.type().name() # ifd, arnold, ris

        if "ifd" in node_type_name:
            cachefile_extension = "ifd"
            #renderer = "mantra"
            renderer = "mantra-shim"
            renderer_arguments = "-V 1a -f"

            outputpicture_param = 'vm_picture'
            outputpicture_mode_param = 'soho_outputmode'
            outputpicture_path_param = 'soho_diskfile'
            tempstorage_path_param = 'vm_tmpsharedstorage'
            tempstorage_name = 'storage'

        elif "arnold" in node_type_name:
            cachefile_extension = "ass"
            renderer = "kick"
            renderer_arguments = "-dw -dp -nostdin"

            outputpicture_param = 'ar_picture'            
            outputpicture_mode_param = 'ar_ass_export_enable'
            outputpicture_path_param = 'ar_ass_file'
            tempstorage_path_param = False # unused
            tempstorage_name = False       # unused

        else:
            cachefile_extension = "rib"
            renderer = "prman"
            renderer_arguments = ""

            outputpicture_param = 'ri_display_0'
            outputpicture_mode_param = 'diskfile'
            outputpicture_path_param = 'soho_diskfile'
            tempstorage_path_param = 'vdbpath'
            tempstorage_name = 'vdbs'
            
        outputpicture_rawvalue = node.parm(outputpicture_param).rawValue()         
        renderfile_folder = "{}_{}_{}".format(basefilename, node.name(), node.type().name())
        renderfile_name = "{}.$F4.{}".format(node.name(), cachefile_extension)
            
        outputpicture_dirname = os.path.dirname(outputpicture_rawvalue)
        renderimage_path = os.path.join(outputpicture_dirname, renderfile_folder)
        
        # setup parameters for file export
        node.parm(outputpicture_mode_param).set(True)
        node.parm(outputpicture_path_param).set("{}/{}".format(renderimage_path, renderfile_name))
        
        if tempstorage_path_param:
            node.parm(tempstorage_path_param).set("{}/{}".format(renderimage_path, tempstorage_name))
        
        # absolute path for folder creation
        outputpicture_evalvalue = node.parm(outputpicture_param).eval()

        # create render folder
        #outputpicture_evalvalue_dirname = os.path.dirname(outputpicture_evalvalue)
        #self.makedir(outputpicture_evalvalue_dirname)
        
        # create export folder
        tempfile_path = os.path.join(os.path.dirname(outputpicture_evalvalue), renderfile_folder)
        self.makedir(tempfile_path)
        
        renderfile_query = []

        # write (ifd) files to disk and start a process afterwards
        if self.export_file(node.parm('execute')):
            
            #all_render_files = [render_file for render_file in sorted(os.listdir(tempfile_path) if cachefile_extension in render_file]
            for render_file in sorted(os.listdir(tempfile_path)):
                ext = render_file.split(".")[-1]
                if cachefile_extension == ext:
                    print(render_file.split("."))
                    number = int(render_file.split(".")[-2])
                    if number >= node_start and number <= node_end and (number - node_start) % node_step == 0:        
                        renderfile_query.append(render_file)
            
            print(renderfile_query)

            # reset param to cache files
            node.parm(outputpicture_mode_param).set(False)

            for render_file in renderfile_query:
                #title = "Frame {}".format(s) if s == e else "Frame {} - {}".format(s, e)
                tempfile_name = os.path.join(tempfile_path, render_file)
                title = "Frame from {}".format(render_file) 

                self.file.write("        Task {{ {} }} -cmds {{\n".format(title))
                #self.file.write("            RemoteCmd {{{} {}/houBatch.py {} {} {} {} {}}} -service {{ {} }} -envkey {{ {} }} -priority {{ {} }} -tags {{ Houdini {} }}\n".format( "/opt/houdini/18.0.416/bin/hython", cur_script_path, hipfile_tmp_fullpath, node.path(), s, e, node_step, service, envkey, self.priority.currentIndex(), self.dict_of_fields["Tags"].text() ))
                self.file.write("            RemoteCmd {{{} {} {} }} -service {{ {} }} -envkey {{ {} }} -priority {{ {} }} -tags {{ Houdini {} }}\n".format( renderer, renderer_arguments, tempfile_name, service, envkey, self.priority.currentIndex(), self.dict_of_fields["Tags"].text() ))
                self.file.write("        }\n")

            self.file.write("    }\n")

            self.file.write("}\n")
            self.file.close()

            # Just to make doubly sure the .alf script is available on disk.
            sleep(1)
            #Dispatch the job to tractor.
            #tractor_host = os.environ.get('TRACTOR_HOST')
            #tractor_port = os.environ.get('TRACTOR_PORT')
            #command = "tractor-spool --engine={}:{} {}".format(tractor_host, tractor_port, jobfull)

        return jobfull


###houdini list functions###
def ExistingRenderers():
    #add some existing renderers
    renderers = ["ifd"]
    #plugin_renderers = ["Redshift_ROP", "ris::22", "arnold","opengl"]
    plugin_renderers = ["arnold","ris::22"]

    for node_type in hou.ropNodeTypeCategory().nodeTypes().values():
        for renderer in plugin_renderers:
            if renderer in node_type.name():
                renderers.append(renderer)

    return renderers

def all_renderable_nodes():
    all_rendernodes = []
    for node in hou.node("/").allSubChildren():
        if  node.type().name() in ExistingRenderers():
                all_rendernodes.append(node)
    return all_rendernodes

def selectedRenderNodes():
    #list all selected renderers
    selection = hou.selectedNodes()
    rendernode_list = []

    for node in selection:
        if  node.type().name() in ExistingRenderers():
            rendernode_list.append(node)
    return rendernode_list

def selectedRopNodes():
    #list of renderers inside of ropnodes
    selection = hou.selectedNodes()
    #ropnode_list = []
    rop_rendernode_list = []

    for ropnode in selection:
        if ropnode.type().name() == "ropnet":
            for rendernode in hou.node(ropnode.path()).allSubChildren():
                if rendernode.type().name() in ExistingRenderers():
                    rop_rendernode_list.append(rendernode)

    return rop_rendernode_list


###call the window###
def go():
    #import sys
    #app = QtWidgets.QApplication(sys.argv())
    global window
    w = QtWidgets.QWidget()
    window = ExportDialog(w)
    window.show()
    #app.exec_()


#if __name__ = "__main__":
#go()


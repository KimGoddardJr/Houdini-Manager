#!/usr/bin/env python

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

for arg in sys.argv:
    

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
    renderfie_name = "{}.$F4.{}".format(node.name(), cachefile_extension)
        
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
    
    # write (ifd) files to disk and start a process afterwards
    if self.export_file(node.parm('execute')):
        
        # reset param to cache files
        node.parm(outputpicture_mode_param).set(False)

        for render_file in sorted(os.listdir(tempfile_path)):
            if cachefile_extension in render_file:
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
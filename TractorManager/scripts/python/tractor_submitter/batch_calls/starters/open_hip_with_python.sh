#!/usr/bin/env bash

PWD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BATCH_SCRIPTS_BASE=$(dirname ${1})

echo @
#run the PyOpenGl_template through a script that hard codes the nodes into it and makes it temporary and callable by houdini
py_filename=${1}/templates/CallWithHip_Template.py

## python script that writes temp_call_OpenGLRender.py from template
/usr/bin/env python ${1}/manipulators/template_rewrite.py ${1} ${py_filename} ${@:3}

source ${BATCH_SCRIPTS_BASE}/ecosystem.env

cd ${HOUDINIDIR}
source houdini_setup

houdini -foreground waitforui ${2} ${BATCH_SCRIPTS_BASE}/CallWithHip.py

# rm ${1}/../temp_call_OpenGLRender.py

#!/usr/bin/env bash

PWD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BATCH_SCRIPTS_PATH=$(dirname ${PWD})
BATCH_SCRIPTS_BASE=$(dirname ${BATCH_SCRIPTS_PATH})

source ${PWD}/call_with_term.sh

#write a temporary command in tmp, that can be opened with a terminal while cotaining all the *args
echo "${BATCH_SCRIPTS_PATH}/starters/open_hip_with_python.sh ${BATCH_SCRIPTS_PATH} ${@:1}" >${BATCH_SCRIPTS_BASE}/OpenHipWithPython_command.sh
chmod +x ${BATCH_SCRIPTS_BASE}/OpenHipWithPython_command.sh

if [[ "$OSTYPE" == "darwin"* ]]; then
    #call generated shell script that calls houdini with the necessary python script
    call_with_term ${BATCH_SCRIPTS_BASE}/OpenHipWithPython_command.sh

    # rm ${PWD}/../temp_call_OpenGLRender.py
    # rm ${BATCH_SCRIPTS_BASE}/tmp_HoudiniGLRender_command.sh
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    ${BATCH_SCRIPTS_BASE}/OpenHipWithPython_command.sh

fi

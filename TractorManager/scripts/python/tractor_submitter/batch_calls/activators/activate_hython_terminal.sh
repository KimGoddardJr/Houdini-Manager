#!/usr/bin/env bash

PWD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

source ${PWD}/call_with_term.sh

#setup environment

${PWD}/create_environment.sh ${1}

RENDER_ARGS="${@:2}"
BATCH_SCRIPTS_PATH=$(dirname ${PWD})
BATCH_SCRIPTS_BASE=$(dirname ${BATCH_SCRIPTS_PATH})

#write a temporary command to open call_command in tmp
echo "${BATCH_SCRIPTS_PATH}/starters/call_hython.sh ${BATCH_SCRIPTS_PATH} ${RENDER_ARGS}" >${BATCH_SCRIPTS_BASE}/tmp_HythonCall_command.sh
# echo "${PWD}/starters/call_hython.sh ${RENDER_ARGS}" >${PWD}/../debug_patxi_now.sh
chmod +x ${BATCH_SCRIPTS_BASE}/tmp_HythonCall_command.sh

#Call Hython
if [[ "$OSTYPE" == "darwin"* ]]; then

    call_with_term ${BATCH_SCRIPTS_BASE}/tmp_HythonCall_command.sh

elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    ${BATCH_SCRIPTS_BASE}/tmp_HythonCall_command.sh

fi

#remove the file again
#rm ${BATCH_SCRIPTS_BASE}/tmp_HythonCall_command.sh

#Open a terminal that calls an expect script that runs a hython script
#${TERMINAL} ${PWD}/call_shell_command.exp ${PWD} ${1} ${2} ${3} ${4}

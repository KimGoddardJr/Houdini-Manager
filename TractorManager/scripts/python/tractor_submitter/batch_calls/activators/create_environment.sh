#!/usr/bin/env bash

PWD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BATCH_SCRIPTS_PATH=$(dirname ${PWD})
BATCH_SCRIPTS_BASE=$(dirname ${BATCH_SCRIPTS_PATH})

export ECO_ENV=${BATCH_SCRIPTS_PATH}/ecosystem-env/
export PYTHONPATH=${BATCH_SCRIPTS_PATH}
export TOOLS=${1}

python ${BATCH_SCRIPTS_PATH}/ecosystem/main.py -t ${TOOLS} -s >${BATCH_SCRIPTS_BASE}/ecosystem.env
chmod 777 ${BATCH_SCRIPTS_BASE}/ecosystem.env

# source ${PWD}/call_with_term.sh

# call_with_term ${PWD}/debug_open_houdini.sh

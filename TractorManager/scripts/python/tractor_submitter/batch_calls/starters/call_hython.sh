#!/usr/bin/env bash

# echo ${1}
# echo ${2}
# echo ${3}
# echo "${@:4}"

PWD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BATCH_SCRIPTS_BASE=$(dirname ${1})

source ${BATCH_SCRIPTS_BASE}/ecosystem.env

cd ${HOUDINIDIR}
source houdini_setup

hython ${1}/houdini_node_processor.py ${2} "${@:3}"

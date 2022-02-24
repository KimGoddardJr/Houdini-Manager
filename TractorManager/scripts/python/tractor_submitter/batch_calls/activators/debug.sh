#!/usr/bin/env bash

PWD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BATCH_SCRIPTS_PATH=$(dirname ${PWD})
BATCH_SCRIPTS_BASE=$(dirname ${BATCH_SCRIPTS_PATH})

echo ${PWD}
echo ${BATCH_SCRIPTS_PATH}
echo ${BATCH_SCRIPTS_BASE}

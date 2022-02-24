#!/usr/bin/env bash

source /tmp/ecosystem.env

cd ${HOUDINIDIR}
source houdini_setup

houdini

# killall Terminal
exit

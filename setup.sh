#!/usr/bin/env bash

HOU_PATH=$1
PCKG_PATH=$1/packages

cp -r TractorManager $PCKG_PATH/
cp TractorManager.json $PCKG_PATH/
cp -r scripts $HOU_PATH/

echo COPIED
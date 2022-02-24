#!/usr/bin/env bash

#Call with term function
call_with_term() {

    #Where is the Terminal App?
    if [[ "$OSTYPE" == "darwin"* ]]; then

        OSX_VERSION=$(echo $OSTYPE | cut -b 7-)

        if [[ $OSX_VERSION < 20 ]]; then
            TERMINAL_PATH="/Applications/Utilities/Terminal.app/Contents/MacOS"
        else
            TERMINAL_PATH="/System/Applications/Utilities/Terminal.app/Contents/MacOS"
        fi

        # Open Terminal App in Gui and launch temp render command
        ${TERMINAL_PATH}/Terminal ${1}

    elif [[ "$OSTYPE" == "linux-gnu" ]]; then
        TERMINAL_PATH="/usr/bin"
        # Open Terminal App in Gui and launch temp render command
        export DISPLAY=:0.0
        ${TERMINAL_PATH}/gnome-terminal ${1}
    fi

}

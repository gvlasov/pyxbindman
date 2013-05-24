#!/bin/bash
if [[ ! -z "$BASH_COMPLETION_DIR" ]]
then
    echo Installing in 1 $BASH_COMPLETION_DIR
elif [[ ! -z "$BASH_COMPLETION_COMPAT_DIR" ]]
then
    echo Installing in 2 $BASH_COMPLETION_COMPAT_DIR
elif [[ -e "/etc/bash_completion.d" ]]
then
    echo Installing in 3 /etc/bash_competion.d
else
    echo Shit
fi


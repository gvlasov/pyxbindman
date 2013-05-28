# Completion script for pyxbindman utility
# Most of the script is for proper handling of special characters
_pyxbindman_get_choices()
{
    search=$(eval echo "$cur" 2>/dev/null || eval echo "$cur'" 2>/dev/null || eval echo "$cur\"" 2>/dev/null || "")
    if [[ ! -z "$cur" && "${COMP_WORDS[COMP_CWORD]:0:1}" == '-' ]];
    then
        # Complete names of options
        py-completion-pyxbindman --option-complete "`echo ${COMP_WORDS[COMP_CWORD]} | sed 's/\-/\\\-/g'`" | 
        grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s#'#\\\'#g" -e 's#"#\\\"#g' -e "}"
    else
        # Complete everything else
        # --cur-word MUST be the first argument
        py-completion-pyxbindman --cur-word "`echo ${COMP_WORDS[COMP_CWORD]} | sed 's/\-/\\\-/g'`" ${COMP_WORDS[@]} | 
        grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s#'#\\\'#g" -e 's#"#\\\"#g' -e "}"
    fi
}


_pyxbindman()
{
    local IFS=$'\n'

    COMPREPLY=()
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"
    local options_to_be_quoted=( [-d]="" [-D]="" )

    local escaped_single_qoute="'\''"
    local i=0
    if [ "${prev}" == '-f' ] || [ "${prev}" == '--file' ];
    then
        COMPREPLY=( $(compgen -f "${cur}") )
    else
        if [[ "${cur:0:1}" == "\"" ]] 
        then
            # Addinionally escape single quotes inside double quotes
            COMPREPLY=( $( compgen -W "$(_pyxbindman_get_choices)" -- "${cur/\'/\'}" ) )
        else
            COMPREPLY=( $( compgen -W "$(_pyxbindman_get_choices)" -- "${cur}" ) )
        fi

        echo $cur $COMPREPLY > shits 
        for entry in ${COMPREPLY[*]}
        do
            if [[ "${cur:0:1}" == "'" ]] 
            then
                # started with single quote, escaping only other single quotes
                # [']bla'bla"bla\bla bla --> [']bla'\''bla"bla\bla bla
                COMPREPLY[$i]="${entry//\'/${escaped_single_qoute}}" 
            elif [[ "${cur:0:1}" == "\"" ]] 
            then
                # started with double quote, escaping all double quotes and all backslashes
                # ["]bla'bla"bla\bla bla --> ["]bla'bla\"bla\\bla bla
                entry="${entry//\\/\\\\}" 
                #COMPREPLY[$i]="${entry//\"/\\\"}" 
            else 
                # no quotes in front, escaping _everything_
                # [ ]bla'bla"bla\bla bla --> [ ]bla\'bla\"bla\\bla\ bla
                entry="${entry//\\/\\\\}" 
                #entry="${entry//\'/\'}" 
                #entry="${entry//\:/\:}" 
                #entry="${entry//\"/\\\"}" 
                #CtrlCOMPREPLY[$i]="${entry// /\\ }"
            fi
            (( i++ ))
        done
    fi
}
complete -o filenames -o bashdefault -F _pyxbindman pyxbindman

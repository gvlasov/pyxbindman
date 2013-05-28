# Completion script for pyxbindman utility
# Most of the script is for proper handling of special characters
_pyxbindman_get_choices()
{
    search=$(eval echo "$cur" 2>/dev/null || eval echo "$cur'" 2>/dev/null || eval echo "$cur\"" 2>/dev/null || "")
    args=("${COMP_WORDS[@]:1:$(( $COMP_CWORD))}")
    if [[ ! -z "$cur" && "${COMP_WORDS[COMP_CWORD]:0:1}" == '-' ]];
    then
        # Complete names of options
        cur_word=`echo ${COMP_WORDS[COMP_CWORD]} | sed 's/\-/\\\-/g'`
        py-completion-pyxbindman --cur-word "${cur_word}" --option-complete ${args[@]} | 
        grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s#'#\\\'#g" -e 's#"#\\\"#g' -e "}"
    else
        # Complete everything else
        # --cur-word MUST be the first argument
        cur_word=${COMP_WORDS[COMP_CWORD]}
        py-completion-pyxbindman --cur-word "${cur_word}" ${args[@]} | 
        grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s#'#\\\'#g" -e 's#"#\\\"#g' -e "}"
    fi
}


_pyxbindman()
{
    local IFS=$'\n'

    COMPREPLY=()
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"

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

    fi
}
complete -o filenames -o bashdefault -F _pyxbindman pyxbindman

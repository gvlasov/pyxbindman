# Completion script for pyxbindman utility
# Most of the script is for proper handlind of special characters
_find_words_command()
{
    search=$(eval echo "$cur" 2>/dev/null || eval echo "$cur'" 2>/dev/null || eval echo "$cur\"" 2>/dev/null || "")
    pyxbindman --get-all-commands |
    grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s/'/\\\'/g" -e 's#"#\\\"#g' -e 's#\:#\\\:#g' -e "}"
    #grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s/'/\\\'/g" -e 's#"#\\\"#g' -e "}"
}
_find_words_keysym()
{
    search=$(eval echo "$cur" 2>/dev/null || eval echo "$cur'" 2>/dev/null || eval echo "$cur\"" 2>/dev/null || "")
    pyxbindman --get-all-keysyms | 
    grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s/'/\\\'/g" -e 's#"#\\\"#g' -e "}"
}
_pyxbindman_get_choices()
{
    search=$(eval echo "$cur" 2>/dev/null || eval echo "$cur'" 2>/dev/null || eval echo "$cur\"" 2>/dev/null || "")
    pyxbindman-completion --completion ${COMP_LINE} | 
    grep -- "^$search" | sed -e "{" -e 's#\\#\\\\#g' -e "s/'/\\\'/g" -e 's#"#\\\"#g' -e "}"
}

_old_shit()
{

    case "$prev" in
        # Delete by command
        -D) COMPREPLY=( $( compgen -W "$(_pyxbindman_get_choices)" -- "$cur" ) )
            ;;
        --delete-by-command) COMPREPLY=( $( compgen -W "$(_find_words_command)" -- "$cur" ) )
            ;;
        # Delete my keysym
        -d) if echo $cur | grep -Eq '^"?m.*'
            then
                COMPREPLY=( $( compgen -W "$(_find_words_keycode)" -- "$cur" ) )
            else
                COMPREPLY=( $( compgen -W "$(_find_words_keysym)" -- "$cur" ) )
            fi
            ;;
        --delete) if echo $cur | grep -Eq '^"?m.*'
            then
                COMPREPLY=( $( compgen -W "$(_find_words_keycode)" -- "$cur" ) )
            else
                COMPREPLY=( $( compgen -W "$(_find_words_keysym)" -- "$cur" ) )
            fi
            ;;
        -f)
            # Completion over files
            COMPREPLY=( $( compgen -f -- "$cur" ) )
            ;;
        --file)
            COMPREPLY=( $( compgen -f -- "$cur" ) )
            ;;
        *)
            # Completion over files and commands
            COMPREPLY=( $( compgen -fac -- "$cur" ) )
            ;;
    esac
}

_pyxbindman()
{
    local IFS=$'\n'

    COMPREPLY=()
    local cur="${COMP_WORDS[COMP_CWORD]}"

    local prev="${COMP_WORDS[COMP_CWORD-1]}"

    local escaped_single_qoute="'\''"
    local i=0

    COMPREPLY=( $( compgen -W "$(_pyxbindman_get_choices)" -- "$cur" ) )

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
    		COMPREPLY[$i]="${entry//\"/\\\"}" 
    	else 
    		# no quotes in front, escaping _everything_
    		# [ ]bla'bla"bla\bla bla --> [ ]bla\'bla\"bla\\bla\ bla
    		entry="${entry//\\/\\\\}" 
    		entry="${entry//\'/\'}" 
    		entry="${entry//\:/\:}" 
    		entry="${entry//\"/\\\"}" 
    		COMPREPLY[$i]="${entry// /\\ }"
    	fi
    	(( i++ ))
    done
}
complete -F _pyxbindman pyxbindman

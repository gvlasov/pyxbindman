pyxbindman
==========

a command line tool for hotkeys management

Installation
------------

    $ git clone https://github.com/Suseika/pyxbindman.git
    $ cd pyxbindman
    # python setup.py install
    # cp completion.sh /etc/bash_completion.d/pyxbindman

    And restart your terminal to enable completion

Basic usage
-----------

This tool works as a frontend for xbindkeys utility, all it does is edit
`xbindkeys`' configurations file(s). 

Two most basic commands are:

Binds command `command` to a key combination

    $ pyxbindman command

Unbinds whatever is bound to a key combination

    $ pyxbindman -d


Those invoke a key-grabbind window and make a hotkey with a desired command
available in your system as soon as you press a key combination.

Usually these two commands are everything you need to manage your hotkeys.

Advanced usage
--------------

Please note that using pyxbindman will remove comments from `.xbindkeysrc` file.

The core feature of this hotkey manager is that you can Tab-complete almost
everything.

Add a new mapping to `~/.xbindkeysrc` and make it immediately available:
    
    $ pyxbindman firefox
    Choose a combination to bind: 
    Combination Control+Alt + apostrophe selected

This and some other commands use the same key detecting window as `xbindkeys -k`.

Delete a mapping for a chosen key combination. `Tab` completes from a list of
keysyms in an `.xbindkeysrc`:

    $ pyxbindman -d "Shift+Alt + o"

Or even by its keycode (completion is available when argument starts with
letter `m`):

    $ pyxbindman -d "m:0x9 c:107"

Delete a mapping by its command name. `Tab` completes from a list of commands in
`.xbindkeysrc`

    $ pyxbindman -D chromium

List all mappings defined in `~/.xbindkeysrc`

    $ pyxbindman
    "chromium" -> Control+Alt + c
    "pidgin" -> Control+Alt + p
    "mocp -G" -> m:0x0 + c:127
    "gnome-terminal -e 'rtorrent'" -> Mod4 + t

Show a particular binding by its command name, keysym or keycode:

    $ pyxbindman -s chromium
    "chromium" -> Control+Alt + c
    $ pyxbindman -s "Mod4 + p"
    "pidgin" -> Control+Alt + p
    $ pyxbindman -s "m:0x0 + c:127"
    "mocp -G" -> m:0x0 + c:127

Without an argument `-s` gets a combination using a key-grabbing window:

    $ pyxbindman -s 
    "chromium" -> Mod4 + c

`-c` flag forces completion to come from commands in `.xbindkeysrc` rather
than from `$PATH` (useful when you need to `-c`hange a command bound to a
particular combination)

    $ pyxbindman -c "chromium --incognito http://facebook.com"
    Choose a combination to bind: 
    Combination Mod4 + p selected

For invocations with each option you can provide path to `.xbindkeysrc` file
using `-f` argument. It defines which file is being edited and used for
getting completion options.

Show bindings in a file

    $ pyxbindman -f ~/oldsystem_copy/.xbindkeysrc 

Add binding to a file

    $ pyxbindman -f /home/anotheruser/.xbindkeysrc chromium "Mod + c"

Remove binding from a file
    $ pyxbindman -f /mnt/remote_host/.xbindkeysrc -D pidgin

... and so on.

Kill xbindkeys

    $ pyxbindman -k

Restart xbindkeys

    $ pyxbindman -r


    
If you like this utility a lot
------------------------------

If you would like to show your appreciation, I'd be glad to receive a good Linux
game of your choosing in Steam : )

Here I am: http://steamcommunity.com/profiles/76561198038302973/

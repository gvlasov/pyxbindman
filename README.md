pyxbindman
==========

Xbindkeys config manager written in Python

Installation
------------

    git clone https://github.com/Suseika/pyxbindman.git
    cd pyxbindman
    sudo python setup.py install
    # To get Tab completion (the core feature, by the way):
    sudo cp completion.sh /etc/bash_completion.d/pyxbindman


Basic usage
-----------

The core feature of this hotkey manager is that you can Tab-complete literally
everything, and that makes defining keyboard bindings with it really quick and
convenient as soon as you get familiar with command's options.

    # Add a new mapping to `~/.xbindkeysrc` and make it immediately available.
    # This command uses the same key detecting window as `xbindkeys -k`.
    $ pyxbindman firefox
    Choose a combination to bind: 
    Combination Control + Alt + apostrophe selected

    # Delete a mapping for a chosen key combination
    # Tab completes from a list of keysyms on already defined bindings
    $ pyxbindman -d Mod4+Shift\ +\ o

    # Delete a mapping by its command name
    # Tab completes from a list of commands on already defined bindings
    $ pyxbindman -D chromium

    # List all mappings defined in .xbindkeysrc
    $ pyxbindman -l
    "chromium" -> Mod4 + c
    "pidgin" -> Mod4 + p
    "mocp -G" -> m:0x0 + c:127
    "gnome-terminal -e 'rtorrent'" -> Mod4 + t
    # Or just find and show a binding by its keysym
    $ pyxbindman -l "Mod4 + c"
    "chromium" -> Mod4 + c
    # Or by command name
    $ pyxbindman -l pidgin
    "pidgin" -> Mod4 + p
    
    # Change a command bound to a particular combination
    $ pyxbindman -c Mod4\ +\ p "pidgin --some-option"
    # Change a particular command bound to a combination
    $ pyxbindman -C "firefox" "chromium"
    # With both -c and -C options pressing Tab on second option inserts the
    # command that is going to be changed, so you can edit it in place.


    
Library
-------

`pyxbindman` comes with a standalone `xbindkeys` Python module which can be
used for tinkering with `xbindkeys` and its config (a little warning: this code
will terminate your currently running `xbindkeys` daemon):

    import os
    from xbindkeys import Xbindkeys
    xb = Xbindkeys()
    print 'Mappings you already defined'
    print xb.get_mappings()

    print 'Enter a combination to be detected by `xbindkeys -k`: '
    code, keysym = xb.read_key()
    print 'You entered a combintation', keysym, 'whose code is', code

    item = xb.get_mapping(code=code, keysym=keysym)
    if item:
        print 'By the way, you have a command "'+item['command']+'" mapped to that combination'
        agreed = raw_input('Do you want to remove it from your xbindkeys file? [y/N]:')
        if agreed[0] in ('Y', 'y'):
            xb.remove_mapping(code=code, keysym=keysym)
    else:
        print 'You don\'t have any commands in your .xbindkeysrc file mapped to that combination'
        agreed = raw_input('Do you want to add a command calling your x-terminal-emulator with that combination to your .xbindkeysrc file? [y/N]:')
        if agreed[0] in ('Y', 'y'):
            xb.add_combination('x-terminal-emulator', code, keysym)
    
   if False:
       # This would save changes you just did to your .xbindkeysrc file
       xb.write_config()
       xb.restart_xbindkeys()

    # And this actually saves changes to another xbindkeysrc file
    # Check your home directory after running this:
    xb2 = Xbindkeys(os.path.join(os.getenv('HOME'), 'ANOHTER_X_BIND_KEYS_RC')
    xb2.add_combination('pavucontrol', keysym='Ctrl + l')
    xb2.add_combination('chromium', keysym='Ctrl+Shift + c')
    xb2.add_combination('x-terminal-emulator', keysym='Alt+Shift + 7')
    xb2.remove_mapping(command='ls')
    xb2.write_config()

If you like this utility a lot
==============================

If you would like to thank me, I'd be glad to
receive a good Linux game of your choosing in Steam : )

Here I am: http://steamcommunity.com/profiles/76561198038302973/

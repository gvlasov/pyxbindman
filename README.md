pyxbindman
==========

Xbindkeys config manager written in Python

Installation
------------

    git clone https://github.com/Suseika/pyxbindman.git
    cd pyxbindman
    sudo python setup.py install


Basic usage
-----------

The core feature of this hotkey manager is that you can Tab-complete literally
everything, and that makes defining keyboard bindings with it really quick and
convenient as soon as you get familiar with command's options.

    # Add a new mapping to `~/.xbindkeysrc` and make it immediately available.
    # This command uses the same key detecting window as `xbindkeys -k`.
    $ pyxbindman firefox
    Choose a combination to bind: 
    Combination Control+Alt + apostrophe selected

    # Delete a mapping for a chosen key combination
    # Tab completes from a list of keysyms in .xbindkeysrc
    $ pyxbindman -d Mod4+Shift\ +\ o

    # Delete a mapping by its command name
    # Tab completes from a list of commands in .xbindkeysrc
    $ pyxbindman -D chromium

    # List all mappings defined in .xbindkeysrc
    $ pyxbindman
    "chromium" -> Mod4 + c
    "pidgin" -> Mod4 + p
    "mocp -G" -> m:0x0 + c:127
    "gnome-terminal -e 'rtorrent'" -> Mod4 + t

    # Peek at a particular binding by its command name, keysym or keycode
    $ pyxbindman -s chromium
    "chromium" -> Mod4 + c
    $ pyxbindman -s "Mod4 + p"
    "pidgin" -> Mod4 + p
    $ pyxbindman -s "m:0x0 + c:127"
    "mocp -G" -> m:0x0 + c:127
    # Provide no arguments to do the same with a key-grabbing window
    $ pyxbindman -s 
    "chromium" -> Mod4 + c

    # -c flag forces completion to come from commands in .xbindkeysrc
    # (useful when you need to change a command bound to a particular
    # combination)
    $ pyxbindman -c "pidgin --some-option"
    Choose a combination to bind: 
    Combination Mod4 + p selected
    
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
------------------------------

If you would like to thank me, I'd be glad to
receive a good Linux game of your choosing in Steam : )

Here I am: http://steamcommunity.com/profiles/76561198038302973/

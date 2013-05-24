import os
from xbindkeys import Xbindkeys

xb = Xbindkeys()
print 'Mappings you already defined'
print xb.get_mappings()

print 'Enter a combination to be detected by `xbindkeys -k`: '
key:ode, keysym = xb.read_key()
print 'You entered a combintation', keysym, 'whose keycode is', keycode

item = xb.get_mapping(keycode=keycode, keysym=keysym)
if item:
    print 'By the way, you have a command "'+item['command']+'" mapped to that combination'
    agreed = raw_input('Do you want to remove it from your xbindkeys file? [y/N]:')
    if agreed[0] in ('Y', 'y'):
        xb.remove_mapping(keycode=keycode, keysym=keysym)
else:
    print 'You don\'t have any commands in your .xbindkeysrc file mapped to that combination'
    agreed = raw_input('Do you want to add a command calling your x-terminal-emulator with that combination to your .xbindkeysrc file? [y/N]:')
    if agreed[0] in ('Y', 'y'):
        xb.add_combination('x-terminal-emulator', keycode, keysym)

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


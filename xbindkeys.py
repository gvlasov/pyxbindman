#!/usr/bin/env python
import os
import re
import sys
import subprocess

DEFAULT_RC = os.path.join(os.getenv('HOME'), '.xbindkeysrc')

class Xbindkeysrc():
    def __init__(self, path=False):
        self.__bindings = False
        self.__path = False
        self.__xbindkeys_was_killed = False
        if path:
            self.__path = path
        else:
            self.get_config_path()

    def get_config_path(self):
        '''
        Returns path to xbindkeys configuration file. If no argument was
        given to __init__, then returs "/home/current_user/.xbindkeysrc".
        '''
        if self.__path:
            return self.__path
        else:
            self.__path = DEFAULT_RC
            return self.__path

    def get_bindings(self, force=False):
        '''
        Returns a list of all bindings stored in object. If there are no
        bindings stored in the object so far, then reads them from file.
        Each item is a dictionary with keys
        'command', 'keycode' and 'keysym'. 

        If force=True, then reads bindings from file even if they are
        already loaded in the object.
        '''
        if self.__bindings != False and not force:
            # If file has already been read, then return the stored bindings
            # (whether the actual file has been changed or not)
            return self.__bindings
        if os.path.isfile(self.get_config_path()):
            # If file exists, it will be parsed line by line

            with open(self.get_config_path()) as file:
                config_text = file.read()

            command, keycode, keysym, self.__bindings = None, None, None, []
            for line in [l.strip() for l in config_text.splitlines()]:
                if re.match('^\s*$', line):
                    continue
                if self.is_command(line):
                    # Code and keysym are optional, but a command has to be for each item of .xbindkeysrc,
                    # so each time we foud a command, we can dump what we found so far to the bindings dictionary
                    if command != None or keysym != None or keycode != None:
                        self._add_binding(command, keycode, keysym)
                    command, keycode, keysym = None, None, None
                    command = line[1:-1]
                elif self.is_keycode(line):
                    keycode = line
                elif self.is_keysym(line):
                    keysym = line
            else:
                # For cases where there is only one item in a file
                if command:
                    self._add_binding(command, keycode, keysym)
        else:
            # Return empty list if file doesn't exist
            self.__bindings = []
        return self.__bindings

    def get_binding(self, command=None, keycode=None, keysym=None):
        '''
        Returns an existing binding identified by command, keycode or keysym. Either one,
        two or all three arguments may be provided, so it will search for a
        binding that meets all of the given criteria.

        If there are several bindings meeting the criteria, then the first one will be returned.
        '''
        if command == None and keycode == None and keysym == None:
            raise Exception('You must specify either a command, a keycode or a keyseym to get an item')
        for item in self.get_bindings():
            if command != None and item['command'] == command or keycode != None and item['keycode'] == keycode or keysym != None and item['keysym'] == keysym:
                return item
        return False

    def read_key(self):
        '''
        Calls `xbindkeys -k` and returns a tuple of 2 items where first item
        is combination's keycode, and the second is combination's keysym. This
        method kills xbindkeys daemon until key combination is provided, and
        then restarts it.
        '''
        self.__xbindkeys_was_killed = True
        self.kill_xbindkeys()
        process = subprocess.Popen(
                ['xbindkeys', '-k'],
                stdout=subprocess.PIPE
                )
        process.wait()
        output = process.communicate()[0]
        keycode, keysym = [s.strip() for s in output.splitlines(True)[-2:]]
        return keycode, keysym

    def binding_exists(self, keycode=None, keysym=None):
        bindings = self.get_bindings()
        if keycode != None:
            for item in bindings:
                if item['keycode'] == keycode:
                    print 'Binding exists by keycode',keycode,'with command',item['command']
                    return True
        if keysym != None:
            for item in bindings:
                if item['keysym'] == keysym:
                    print 'Binding exists by keysym',keysym,'with command',item['command']
                    return True
        return False

    def is_command(self, line):
        '''
        Checks if a trimmed line is a valid command for xbindkeys item.
        '''
        line = line.strip()
        return line[0] == '"' and line[-1:] == '"'

    def is_keycode(self, line):
        '''
        Checks if a trimmed line is a valid keycode for xbindkeys item.
        '''
        line = line.strip()
        return re.match('m:\dx[\da-f]{1,2} \+ c:\d+$', line)

    def is_keysym(self, line):
        '''
        Checks if a trimmed line is a valid keysym for xbindkeys item.
        '''
        line = line.strip()
        return re.match('[\d_\w]+(\s*\+\s*[\d_\w]+)*', line)

    def _add_binding(self, command, keycode=None, keysym=None, **kwargs):
        if not keycode and not keysym:
            raise BindingException('Either keycode or a keysym must be provided',kwargs)
        self.__bindings.append({
            'command': command,
            'keycode': keycode,
            'keysym': keysym
        })

    def xbindkeys_was_killed(self):
        return self.__xbindkeys_was_killed

    def add_binding(self, command, keycode=None, keysym=None):
        '''
        Adds a new binding described by a command, and keycode and keysym (or both).
        This method does not directly add the binding to the configuration
        file, it just saves it in the object. Use Xbindkeysrc#write_config to
        write all the added combinations to the config file.
        '''
        if self.binding_exists(keycode=keycode, keysym=keysym):
            raise BindingException('Binding for %s is already defined' % 
                    ' '.join([param for param in (keycode, keysym) if param != None]))
        self._add_binding(command=command, keycode=keycode, keysym=keysym)

    def clear_bindings(self):
        '''
        Removes all bindings defined in this object
        '''
        self.__bindings = []

    def remove_binding(self, command=None, keycode=None, keysym=None):
        '''
        Removes an item from bindings list by its command, keycode or keysym.

        Returns the removed item, or False of no item was removed
        '''
        bindings = self.get_bindings()[:]
        if command != None:
            for item in bindings:
                if item['command'] == command:
                    self.__bindings.remove(item)
                    return item
        if keycode != None:
            for item in bindings:
                if item['keycode'] == keycode:
                    self.__bindings.remove(item)
                    return item
        if keysym != None:
            for item in bindings:
                if item['keysym'] == keysym:
                    self.__bindings.remove(item)
                    return item
        return False

    def restart_xbindkeys(self):
        '''
        Restarts xbindkeys daemon if it is running, or starts it if it is not
        running. Restarting xbindkeys daemon is needed to reload config file.
        '''
        with open(os.devnull, 'wb') as devnull:
            if subprocess.call(['pidof', 'xbindkeys'], stdout=devnull) == 0:
                subprocess.call(['killall', '-HUP', 'xbindkeys'], stdout=devnull, stderr=devnull)
            else:
                subprocess.call('xbindkeys')
        self.__xbindkeys_was_killed = False

    def kill_xbindkeys(self):
        '''
        Kills xbindkeys daemon process
        '''
        with open(os.devnull, 'wb') as devnull:
            subprocess.call(['killall', '-9', 'xbindkeys'], stdout=devnull, stderr=devnull)

    def command_completer(self):
        '''
        Method used by argcomplete module to provide completion of commands
        from .xbindkeysrc file
        '''
        return [item['command'] for item in self.get_bindings()]

    def write_config(self, path=None):
        '''
        Saves configuration from object's temporary internal representation to
        a permanent config file. Path to config file is defined by the first
        argument of object'c costructor.
        '''
        if path == None:
            path = self.get_config_path()
        f = open(path,'w')
        for item in self.__bindings:
            f.write('"'+item['command']+'"\n')
            if item['keycode']:
                f.write('\t'+item['keycode']+'\n')
            if item['keysym']:
                f.write('\t'+item['keysym']+'\n')
            f.write('\n')

    def show_binding(self, command=None, keysym=None, keycode=None):
        if command == None and keysym == None and keycode == None:
            raise ValueError('You must provide one of command, keysym or keycode arguments')
        item = self.get_binding(command=command, keysym=keysym, keycode=keycode)
        if not item:
            return ''
        return '"'+item['command']+'" -> '+(item['keysym'] if item['keysym'] else item['keycode']) 

    def __repr__(self):
        '''
        Translating the object to string form shows bindings defined in it
        '''
        return '\n'.join(
            ['"'+item['command']+'" -> '+(item['keysym'] if item['keysym'] else item['keycode']) 
                for item in self.get_bindings()]
            )

class BindingException(ValueError):
    pass

class EnvironmentError(ValueError):
    pass

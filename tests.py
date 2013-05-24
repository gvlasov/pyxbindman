import unittest
import os
import sys
import subprocess
from subprocess import Popen, PIPE
from xbindkeys import Xbindkeysrc, BindingException

test_config_text = '''
"gvim"
    m:0x40 + c:55
    Mod4 + v
# COMMENT
"chromium"
    m:0x40 + c:54
    Mod4 + c

"mocp -G"
    m:0x0 + c:127
    Pause

"sudo halt"
    m:0xd + c:43
    Control+Shift+Alt + h

"poptran"
    m:0x0 + c:104
    KP_Enter

"pyxbindman -r && naughtify 'xbindkeys restarted'"
    m:0x40 + c:21
    Mod4 + equal

"skype"
    m:0x40 + c:39
    Mod4 + s

"pidgin"
    m:0x40 + c:33
    Mod4 + p

"gnome-terminal -e 'mc'"
    m:0x40 + c:57
    Mod4 + n

"gnome-terminal -e 'pyxbindman'"
    m:0x40 + c:20
    Mod4 + minus

"gnome-terminal -e 'pyxbindman -D'"
    m:0x41 + c:20
    Shift+Mod4 + minus

"sudo reboot"
    m:0xd + c:27
    Control+Shift+Alt + r

"crawl-tiles"
    m:0x41 + c:54
    Shift+Mod4 + c

"ls -l"
    Control + 8

'''
class Xbindkeys(unittest.TestCase):

    path_counter = 0

    @classmethod
    def setUpClass(self):
        self.file_prefix = 'TEST_XBINDKEYS_RC_'
        self.path_counter = 0

    @classmethod
    def create_config(self):
        '''
        Creates a new test config file with predefined content and returns path to it.
        '''
        path = self.get_path()
        with open(path, 'w+') as file:
            file.write(test_config_text)
        print '+ Config file',path,'created'
        return path

    @classmethod
    def get_path(self, num=None):
        '''
        Generates a new unique path for a config file
        '''
        if num == None:
            self.path_counter += 1
            return os.path.join(
                    os.getenv('HOME'),
                    self.file_prefix+str(self.path_counter)
                    )
        else:
            return os.path.join(
                    os.getenv('HOME'),
                    self.file_prefix+str(num)
                    )

    @classmethod
    def tearDownClasr(self):
        for i in range(1, self.path_counter+1):
            path = self.get_path(i)
            print '- Config file',path,'removed'
            os.remove(path)

class Library(Xbindkeys):

    def testReadConfig(self):
        xb = Xbindkeysrc(self.create_config())
        self.assertTrue(len(xb.get_bindings()) == 13)

    def testAdd(self):
        xb = Xbindkeysrc(self.create_config())
        xb.add_binding(command='ls', keycode='m:0x9 + c:12')
        self.assertTrue(
                not xb.binding_exists(keysym='Alt + 4')
                )
        xb.add_binding(command='ps -e', keysym='Alt + 4')
        xb.write_config()

    def testWrongAdd(self):
        xb = Xbindkeysrc(self.create_config())
        self.assertRaises(
                BindingException, 
                xb.add_binding, 
                command='ls',
                )
        self.assertRaises(
                TypeError, 
                xb.add_binding, 
                keycode='m:0xd + c:27',
                )
        self.assertRaises(
                TypeError, 
                xb.add_binding, 
                keysym='Shift+k',
                )

class Frontend(Xbindkeys):
    '''
    Tests how pyxbindman works. Each test creates a new cofig file that is
    filled with the same predifined bindings.
    '''

    def test_adding(self):
        path = self.create_config()

        add_binding_process = Popen(
                ['./pyxbindman', '-f', path],
                stdin=PIPE
                )
        add_binding_process.communicate(input='deep_shit\n')
        with open(path) as file:
            self.assertTrue('deep_shit' in file.read())

    def test_listing(self):
        path = self.create_config()
        list_process = Popen(
                ['./pyxbindman', '-l', '-f', path],
                stdout=PIPE
                )
        stdout = list_process.communicate()[0]
        for i,line in enumerate(stdout.splitlines()):
            print i,line
        return
        self.assertEqual(
                len(stdout.splitlines()), 13
                )

    def test_deleting(self):
        path = self.create_config()
        Popen(
                ['./pyxbindman', '-d', 'Alt+Ctrl + j', '-f', path],
                stdout=PIPE
                )
        Popen(
                ['./pyxbindman', '-d', 'm:0x9 + c:12', '-f', path],
                stdout=PIPE
                )
        Popen(
                ['./pyxbindman', '-D', 'poptran', '-f', path],
                stdout=PIPE
                )

    def test_amount_of_bindings_after_adding(self):
        path = super(Frontend, self).create_config()
        xb = Xbindkeysrc(path)
        self.assertTrue(xb.get_config_path() == path)

    def test_interactive(self):
        path = self.create_config()
        process = Popen(
                ['./pyxbindman', '-i', '-f', path],
                stdin=PIPE
                )
        process.communicate(input='d\nf\nq\n')

    def test_change(self):
        path = self.create_config()
        process = Popen(
                ['./pyxbindman', '-f', path, '-c', 'Control + 8', 'ls'],
                stdin=PIPE
                )
        process = Popen(
                ['./pyxbindman', '-f', path, '-C', 'ls', 'ls -a'],
                stdin=PIPE
                )

    def test_interactive(self):
        path = self.create_config()
        process = Popen(
                ['./pyxbindman', '-l', 'Pause', '-f', path],
                stdin=PIPE
                )

if __name__ == '__main__':
    unittest.main()

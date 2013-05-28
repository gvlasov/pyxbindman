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
        self.assertTrue(len(xb.get_bindings()) == 4)

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
    filled with the same predefined bindings.
    '''

    def test_adding(self):
        path = self.create_config()

        cmd = ['./pyxbindman',  '-f', path, 'deep_shit']
        print cmd, 'AAAAAA'
        subprocess.call(cmd)
        with open(path) as file:
            self.assertTrue('deep_shit' in file.read())

    def test_listing(self):
        path = self.create_config()
        cmd = './pyxbindman -f "' + path +'" -s'

    def test_deleting(self):
        path = self.create_config()
        subprocess.call(['./pyxbindman',  '-f', path, '-d', 'Alt+Ctrl + j'])
        subprocess.call(['./pyxbindman',  '-f', path, '-d', 'm:0x9 + c:12'])
        subprocess.call(['./pyxbindman',  '-f', path, '-D', 'poptran'])

    def test_change(self):
        path = self.create_config()
        subprocess.call(['./pyxbindman',  '-f', path, '-c', 'gvim --hello'])
        with open(path) as file:
            self.assertTrue('gvim --hello' in file.read())


class Completion(Xbindkeys):
    def test_completion(self):
        pass


if __name__ == '__main__':
    unittest.main()

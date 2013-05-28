#!/usr/bin/env python

from distutils.core import setup
from shutil import copyfile
import os
import sys

setup(
        name='pyxbindman',
        version='1.0',
        description='A command line hotkeys manager running over xbindkeys',
        long_description=open('README.md', 'r').read(),
        license='BSD',
        author='Georgy Vlasov',
        author_email='wlasowegor@gmail.com',
        url='https://github.com/Suseika/pyxbindman',
        packages=[],
        py_modules=['xbindkeys'],
        scripts=['pyxbindman', 'py-completion-pyxbindman'],
        )
#if os.path.isdir('/etc/bash_completion.d'):
#    copyfile('completion.sh', '/etc/bash_completion.d/pyxbindman')
#else:
#    print '! ATTENTION: bash completion could not be installed'
#    sys.exit(1)

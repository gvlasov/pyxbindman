#!/usr/bin/env python

from distutils.core import setup

setup(
        name='pyxbindman',
        version='1.0',
        description='An easy-to-use Python utility for managing xbindkeys\' configuration files',
        long_description=open('README.md', 'r').read(),
        license='BSD',
        author='Georgy Vlasov',
        author_email='wlasowegor@gmail.com',
        url='https://github.com/Cookson/pyxbindman',
        packages=[],
        py_modules=['xbindkeys'],
        scripts=['pyxbindman', 'pyxbindman-completion'],
        )

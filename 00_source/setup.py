from distutils.core import setup
import py2exe
import selenium

setup(
    windows=['Main.py'],
    options =
        {'py2exe':
            {
        'packages': ['selenium']
            }
        }
    )

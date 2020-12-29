#! python3.8.5
from setuptools import setup
import os
import py2exe
import matplotlib

VERSION = '1.0.0'

includes = ["sip",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "numpy",
            "matplotlib.backends.backend_qt5agg",
            "scipy",
            "scipy.sparse.csgraph._validation",
            "scipy.special._ufuncs_cxx",
            "pandas"]

datafiles = [("platforms", ["C:\\Python38\\Lib\\site-packages\\PyQt5\\plugins" +
                            "\\platforms\\qwindows.dll"]),
             ("", [r"c:\windows\syswow64\MSVCP100.dll",
                   r"c:\windows\syswow64\MSVCR100.dll"])] + \
            matplotlib.get_py2exe_datafiles()

setup(
    name='trademax-api-client',
    version=VERSION,
    packages=['trademax-api-client'],
    url='https://github.com/mjovanc/trademax-api-client',
    license='MIT',
    windows=[{"script": "main.py"}],
    scripts=['main.py'],
    data_files=datafiles,
    install_requires=[
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'configparser==5.0.1',
        'idna==2.10',
        'PyQt5==5.15.1',
        'PyQt5-sip==12.8.1',
        'PyQt5-stubs==5.14.2.2',
        'pytz==2020.4',
        'qtgui==0.0.1',
        'qtwidgets==0.16',
        'requests==2.24.0',
        'urllib3==1.25.10'
    ],
    options={
        'py2exe': {
            'includes': includes,
        }
    }
)

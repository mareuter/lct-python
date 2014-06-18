#!/usr/bin/env python2

# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

try:
    from setuptools import setup
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    have_setuptools = False
    
from distutils.command.install_data import install_data
import distutils.command.build
from distutils.cmd import Command

import glob
import os
import stat

PACKAGE = 'lct'
MAJOR = 0
MINOR = 4
PATCH = 0
try:
    VERSION = "%d.%d.%d" % (MAJOR, MINOR, PATCH)
except TypeError:
    VERSION = "%d.%d.%s" % (MAJOR, MINOR, PATCH)

# Pete Shinner's distutils data file fix... from distutils-sig
#  data installer with improved intelligence over distutils
#  data files are copied into the project directory instead
#  of willy-nilly
class smart_install_data(install_data):   
    def run(self):
        # need to change self.install_dir to the library dir
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return install_data.run(self)

# Function to check timestamps for file creation
def isNewer(src, target):
    if not os.path.exists(target):
        return True
    src_mtime = os.stat(src)[stat.ST_MTIME]
    target_mtime = os.stat(target)[stat.ST_MTIME]
    if src_mtime > target_mtime:
        return True
    else:
        return False

# Function to run command calls
def exec_cmd(cmd):
    import subprocess as sub
    proc = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, shell=True)
    (stdout, stderr) = proc.communicate()
    proc.wait()
    if proc.returncode:
        print stdout
    
def write_version(filename="version.py"):
    vfile = open(os.path.join(PACKAGE, filename), 'w')
    try:
        vfile.write("version='%s'" % VERSION)
    finally:
        vfile.close()
    
# Make a command class to build PyQt/Qt specific stuff
class build_qt(Command):
    description="Build PyQt/Qt resources and UIs"
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _make_ui(self, idir, odir):
        import dircache
        uifiles = [f for f in dircache.listdir(idir) if f.endswith('.ui')]
        for uifile in uifiles:
            pyuifile = "ui_"+uifile.split('.')[0]+".py"
            uifile = os.path.join(idir, uifile)
            pyuifile = os.path.join(odir, pyuifile)
            if isNewer(uifile, pyuifile): 
                pyuic_cmd = "pyuic4 --from-imports -o %s %s" % (pyuifile, uifile)
                print pyuic_cmd
                exec_cmd(pyuic_cmd)

    def run(self):
        # Make resources
        qtr = ["res/main_resources.qrc", "res/widget_resources.qrc"]
        pyqtr = ["lct/ui/main_resources_rc.py", "lct/ui/widgets/widget_resources_rc.py"]
        import itertools
        for rc, pyrc in itertools.izip(qtr, pyqtr):
            if isNewer(rc, pyrc):
                pyrcc_cmd = "pyrcc4 -o %s %s" % (pyrc, rc)
                print pyrcc_cmd
                exec_cmd(pyrcc_cmd)
            
        # Make dialogs
        udirs = ('ui', os.path.join('ui','widgets'))
        for udir in udirs:
            indir = os.path.join('res', udir)
            outdir = os.path.join(PACKAGE, udir)
            self._make_ui(indir, outdir)
        
old_cmds = distutils.command.build.build.sub_commands
new_cmds = [('build_qt', None)]
new_cmds.extend([x for x in old_cmds])
distutils.command.build.build.sub_commands = new_cmds

CLASSIFIERS = [
"Programming Language :: Python",
"Programming Language :: Python :: 2",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
"Development Status :: 3 - Alpha",
"Intended Audience :: Science/Research",
"Intended Audience :: End Users/Desktop",
"Topic :: Scientific/Engineering :: Astronomy"]

install_requires = []
if have_setuptools:
    install_requires.append("pyephem")
    install_requires.append("qdarkstyle")
    install_requires.append("tzlocal")

if __name__ == "__main__":
    write_version()
    setup(name = PACKAGE,
          version = VERSION,
          description = 'Lunar Club Tools',
          author = 'Michael Reuter',
          author_email = 'mareuternh@gmail.com',
          url = 'https://github.com/mareuter/lct-python',
          license = 'MIT',
          classifiers = CLASSIFIERS,
          long_description = os.linesep+open("README.rst").read(),
          platforms="Linux,OSX,Windows",
          cmdclass = {'install_data': smart_install_data,
                      'build_qt': build_qt},
          data_files = [ ('lct/ui', glob.glob('res/ui/*.ui')),
                        ('lct/ui/widgets', glob.glob('res/ui/widgets/*.ui')),
                        ('lct/db', glob.glob('lct/db/*.db')),
                        ('lct/images', glob.glob('res/images/*.svg')) ],
          package_dir = {'lct': 'lct',
                         'lct.ui': 'lct/ui',
                         'lct.ui.widgets': 'lct/ui/widgets',
                         'lct.features': 'lct/features',
                         'lct.utils': 'lct/utils'},
          packages = ['lct',
                      'lct.features',
                      'lct.ui',
                      'lct.ui.widgets',
                      'lct.utils'],
          scripts = ['scripts/lunar_club_tools.py'],
          install_requires=install_requires)

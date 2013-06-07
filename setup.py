#!/usr/bin/env python

# $Id$

from distutils.core import setup
from distutils.command.install_data import install_data
import distutils.command.build
from distutils.cmd import Command
import glob
import os
import stat

PACKAGE = 'lct'
MAJOR = 0
MINOR = 2
PATCH = 0
VERSION = "%d.%d.%d" % (MAJOR, MINOR, PATCH)

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
                pyuic_cmd = "pyuic4 -o %s %s" % (pyuifile, uifile)
                print pyuic_cmd
                exec_cmd(pyuic_cmd)

    def run(self):
        # Make resources
        qtr = "res/resources.qrc"
        pyqtr = "%s/resources_rc.py" % PACKAGE
        if isNewer(qtr, pyqtr):
            pyrcc_cmd = "pyrcc4 -o %s %s" % (pyqtr, qtr)
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

if __name__ == "__main__":
    write_version()
    setup(name = PACKAGE,
          version = VERSION,
          description = 'Lunar Club Tools',
          author = 'Michael Reuter',
          author_email = 'mareuternh@gmail.com',
          license = 'MIT Academic',
          cmdclass = {'install_data': smart_install_data,
                      'build_qt': build_qt},
          data_files = [ ('lct/ui', glob.glob('res/ui/*.ui')),
                        ('lct/ui/widgets', glob.glob('res/ui/widgets/*.ui')),
                        ('lct/db', '%s/db' % PACKAGE),
                        ('lct/images', glob.glob('res/images/*.svg')) ],
          package_dir = {'lct': 'lct',
                         'lct.ui': 'lct/ui',
                         'lct.features': 'lct/features',
                         'lct.utils': 'lct/utils'},
          packages = ['lct',
                      'lct.features',
                      'lct.ui',
                      'lct.utils'])
          #scripts = ['bin/planet_weight_calc.py'])

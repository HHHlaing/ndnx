#! /usr/bin/env python
# encoding: utf-8

# doxygen docs
from waflib.Build import BuildContext
class doxy (BuildContext):
    cmd = "doxygen"
    fun = "doxygen"

def configure (conf):
    conf.load ('doxygen')
    conf.check_doxygen(mandatory=False)

def options (opt):
    opt.load ('doxygen', tooldir=['waf-tools'])

def doxygen (bld):
    if not bld.env.DOXYGEN:
        bld.fatal ("ERROR: cannot build documentation (`doxygen' is not found in $PATH)")
    bld (features="doxygen",
         doxyfile='doc/doxygen.conf')

# doxygen docs
from waflib.Build import BuildContext
class sphinx (BuildContext):
    cmd = "sphinx"
    fun = "sphinx"

def sphinx (bld):
    bld.load('sphinx_build', tooldir=['waf-tools'])

    bld (features="sphinx",
         outdir = "doc/html",
         source = "doc/source/conf.py")


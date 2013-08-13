# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-
VERSION='0.1'

from waflib import Build, Logs, Utils, Task, TaskGen, Configure

def options(opt):
    opt.load('compiler_cc')
    opt.load('flags ssl docs', tooldir=['build-tools'])

def configure(conf):
    conf.load("compiler_cc flags ssl")
    conf.define("NDNX_VERSION", VERSION)
    conf.check_ssl()
    conf.write_config_header('config.h')
    conf.load ('docs')

def build (bld):
    libndn_cxx = bld (
        target="ndn-c",
        features=['cc', 'cshlib'],
        source = bld.path.ant_glob(['ndn-c/**/*.c',
                                    'ndn-c/libndn-c.pc.in']),
        use = 'SSL',
        includes = [".", "ndn-c"],
        )

    # headers = bld.path.ant_glob(['ndn.cxx.h', 'ndn.cxx/**/*.h'])
    # bld.install_files("%s" % bld.env['INCLUDEDIR'], headers, relative_trick=True)

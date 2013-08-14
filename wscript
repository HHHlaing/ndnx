# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-
VERSION='0.1'

from waflib import Build, Logs, Utils, Task, Node, TaskGen, Configure
import os

def options(opt):
    opt.load('compiler_c')
    opt.load('flags openssl headers docs', tooldir=['waf-tools'])

def configure(conf):
    conf.load("compiler_c flags openssl headers")
    conf.define("NDNX_VERSION", VERSION)

    conf.check_ssl()
    conf.check_cc(lib='resolv', uselib_store='RESOLV', define_name='HAVE_RESOLV')
    conf.env['SH'] = getattr(conf.environ, 'SH', '/bin/sh')

    conf.check_cfg(package='expat', args=['--cflags', '--libs'], uselib_store='EXPAT', mandatory=False)
    conf.check_cc(lib='pcap', uselib_store='PCAP', define_name='HAVE_PCAP', mandatory=False)

    conf.env['DEFINES_COPY'] = conf.env['DEFINES']
    
    conf.write_config_header('config.h')
    conf.load ('docs')

def build (bld):
    ##########################################################
    #                       NDN C API                        #
    ##########################################################

    # "Create" and install header files
    bld (features = ['ndn_headers'],
         target = "headers",
         source = bld.path.ant_glob(['ndn-c/**/*.h'])
         )

    # Build NDN C API
    bld(target="ndn-c-objects",
        features = ['c'],
        source = bld.path.ant_glob(['ndn-c/**/*.c',
                                    'ndn-c/libndn-c.pc.in']),
        use = 'headers SSL RESOLV',
        includes = [".", "ndn-c"])

    # Shared library for NDN C API
    bld(target="lib/ndn-c", features=['c', 'cshlib'], use = "ndn-c-objects")

    # # Static library for NDN C API
    # bld(target="lib/ndn-c", features=['c', 'cstlib'], use = "ndn-c-objects", install_path="${LIBDIR}")
    
    bld.recurse(['apps', 'sync'])

    ##########################################################
    #                      NDN Daemon                        #
    ##########################################################

    bld(target="bin/ndnd",
        features = ['c', 'cprogram'],
        source = bld.path.ant_glob(['ndnd/*.c']),
        use = 'lib/ndn-c',
        includes = ["."])
    
    ##########################################################
    #                       NDN Repo                         #
    ##########################################################

    bld(target="bin/ndnr",
        features = ['c', 'cprogram'],
        source = bld.path.ant_glob(['ndnr/*.c']),
        use = 'lib/ndn-c ../lib/ndn-c-sync',
        includes = ["."])


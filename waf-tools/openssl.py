#! /usr/bin/env python
# encoding: utf-8

'''

When using this tool, the wscript will look like:

	def options(opt):
	        opt.tool_options('openssl', tooldir=['waf-tools'])

	def configure(conf):
		conf.load('compiler_c openssl')
        conf.check_ssl(var='SSL', mandatory=True)

	def build(bld):
		bld(source='main.cpp', target='app', use='SSL')

Options are generated, in order to specify the location of OpenSSL includes/libraries.


'''
from waflib import Configure, Options

SSL_CHECK_CODE = """
#include <openssl/crypto.h>
#include <stdio.h>

int main(int argc, char **argv) {
	(void)argc;
        printf ("%s", argv[0]);

	return 0;
}
"""

@Configure.conf
def check_ssl(self,*k,**kw):
        root = k and k[0] or kw.get('path',None) or Options.options.ssl
        mandatory = kw.get('mandatory', True)
        var = kw.get('var', 'SSL')

        if root:
                testApp = self.check_cc (lib=['ssl', 'crypto'],
                                         header_name='openssl/crypto.h',
                                         define_name='HAVE_%s' % var,
                                         uselib_store=var,
                                         mandatory = mandatory,
                                         cflags="-I%s/include" % root,
                                         linkflags="-L%s/lib" % root,
                                         execute = True, fragment = SSL_CHECK_CODE, define_ret = True)
        else:
                testApp = libcrypto = self.check_cc (lib=['ssl', 'crypto'],
                                                     header_name='openssl/crypto.h',
                                                     define_name='HAVE_%s' % var,
                                                     uselib_store=var,
                                                     mandatory = mandatory,
                                                     execute = True, fragment = SSL_CHECK_CODE, define_ret = True)

def options(opt):
        """
        OpenSSL options
        """
        opt = opt.add_option_group("OpenSSL Options")
        opt.add_option('--ssl',type='string',default='',dest='ssl',help='''path to OpenSSL library''')

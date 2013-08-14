#! /usr/bin/env python
# encoding: utf-8

from waflib import TaskGen, Task, Node, Utils
import re

@TaskGen.feature('ndn_headers')
def feature_ndn_headers(self):
    install_path=getattr(self,'install_path','${INCLUDEDIR}')

    headerpath = self.path.get_bld().make_node("ndn")
    headerpath.mkdir()
    
    inputs=[]
    outputs=[]
    for file in Utils.to_list (self.source):
        if isinstance(file,Node.Node):
            header=file
        else:
            header=self.path.find_resource(file)
        inputs.append(header)

        realheader = headerpath.make_node(re.sub('ndn_','',header.name, count=1))
        outputs.append(realheader)

        tsk=self.create_task('ndn_header',header,realheader)
                                
    if install_path:
        self.bld.install_files("%s/ndn" % install_path, outputs)
    
class ndn_header(Task.Task):
    color='PINK'
    def run(self):
        self.outputs[0].write(self.inputs[0].read('rb'),'wb')

@TaskGen.extension('.h')
def process_h(self,node):
	node.sig=Utils.h_file(node.abspath())

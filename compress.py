#!/usr/bin/python

# -*- coding: utf-8 -*

import tarfile
import os
import sys

def make_tar(src_dir, dest_dir, compression):
    if compression:
        dest_ext = '.' + compression
    else:
        dest_ext = ''
    arcname = os.path.basename(src_dir)
    dest_name = '%s.tar%s' % (arcname, dest_ext)
    dest_path = os.path.join(dest_dir, dest_name)
    print 'arcname' , arcname
    print 'dest_name' , dest_name
    print 'dest_path' , dest_path
    if compression:
        dest_cmp = ':' + compression
    else:
        dest_cmp = ''
    out = tarfile.TarFile.open(dest_path, 'w'+dest_cmp)
    out.add(src_dir, arcname)
    out.close( )
    return dest_path

if __name__ == '__main__':
    argvs = sys.argv
    make_tar(argvs[1], argvs[2], 'gz')

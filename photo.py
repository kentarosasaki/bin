#!/usr/bin/env python
# coding=utf-8
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
photo.py: rename photo file name
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import os
import sys


def rename_files(path, ext = "jpg"):
  i = 1
  files = [os.path.join(path, name) for name in os.listdir(path)]
  files.sort(key=os.path.getmtime)
  for f in files:
    file_ext = os.path.splitext(f)[-1].lower()[1:]
    if ext.lower() == file_ext:
      d = ".".join([os.path.join(path, "%05d" % i), ext])
      os.rename(f, d)
      i += 1
      print("src:    %s" % f)
      print("rename: %s" % d)


def main():
  path = sys.argv[1]
  ext = sys.argv[2]
  rename_files(path, ext)


if __name__ == '__main__':
  main()

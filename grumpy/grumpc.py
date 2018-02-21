#!/usr/bin/env python
# coding=utf-8

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""A Python -> Go transcompiler."""

from __future__ import unicode_literals

import argparse
import os
import sys
import textwrap
from StringIO import StringIO

import grumpy
from grumpy.compiler import block
from grumpy.compiler import imputil
from grumpy.compiler import stmt
from grumpy.compiler import util
from grumpy.vendor import pythonparser


def honor_pep3147(script_path, stream):
  assert script_path.endswith('.py')
  GOPATH_PATTERN = 'gopath/src/__python__/'
  magic_tag = 'grumpy-' + grumpy.__version__.replace('.', '')  # cpython-27
  script_folder = os.path.dirname(os.path.abspath(script_path))
  script_basename = script_path.rpartition('.')[0]
  bytecompiled_name = '{script_basename}.{magic_tag}.{suffix}'.format(  # hello.cpython-27-PYTEST.pyc
    script_basename=script_basename,
    magic_tag=magic_tag,
    suffix='pyc',
  )
  base_folder = os.path.join(
    script_folder,
    '__pycache__',
    bytecompiled_name,
    GOPATH_PATTERN,
  )
  module_folder = os.path.join(base_folder, script_basename)
  if not os.path.exists(module_folder):
    os.makedirs(module_folder)

  gopath_script_filename = os.path.join(base_folder, script_path)
  with open(gopath_script_filename, 'w') as gopath_script_file:
    with open(script_path) as original_file:
      gopath_script_file.writelines(original_file.readlines())

  module_filename = os.path.join(module_folder, 'module.go')
  with open(module_filename, 'w') as module_file:
    module_file.writelines(stream.readlines())


def main(script=None, modname=None, pep3147=False):
  assert script and modname, 'Script "%s" or Modname "%s" is empty' % (script,modname)

  gopath = os.getenv('GOPATH', None)
  if not gopath:
    print >> sys.stderr, 'GOPATH not set'
    return 1

  with open(script) as py_file:
    py_contents = py_file.read()
  try:
    mod = pythonparser.parse(py_contents)
  except SyntaxError as e:
    print >> sys.stderr, '{}: line {}: invalid syntax: {}'.format(
        e.filename, e.lineno, e.text)
    return 2

  # Do a pass for compiler directives from `from __future__ import *` statements
  try:
    future_node, future_features = imputil.parse_future_features(mod)
  except util.CompileError as e:
    print >> sys.stderr, str(e)
    return 2

  importer = imputil.Importer(gopath, modname, script,
                              future_features.absolute_import)
  full_package_name = modname.replace('.', '/')
  mod_block = block.ModuleBlock(importer, full_package_name, script,
                                py_contents, future_features)

  visitor = stmt.StatementVisitor(mod_block, future_node)
  # Indent so that the module body is aligned with the goto labels.
  with visitor.writer.indent_block():
    try:
      visitor.visit(mod)
    except util.ParseError as e:
      print >> sys.stderr, str(e)
      return 2

  file_buffer = StringIO()
  writer = util.Writer(file_buffer)
  tmpl = textwrap.dedent("""\
      package $package
      import πg "grumpy"
      var Code *πg.Code
      func init() {
      \tCode = πg.NewCode("<module>", $script, nil, 0, func(πF *πg.Frame, _ []*πg.Object) (*πg.Object, *πg.BaseException) {
      \t\tvar πR *πg.Object; _ = πR
      \t\tvar πE *πg.BaseException; _ = πE""")
  writer.write_tmpl(tmpl, package=modname.split('.')[-1],
                    script=util.go_str(script))
  with writer.indent_block(2):
    for s in sorted(mod_block.strings):
      writer.write('ß{} := πg.InternStr({})'.format(s, util.go_str(s)))
    writer.write_temp_decls(mod_block)
    writer.write_block(mod_block, visitor.writer.getvalue())
  writer.write_tmpl(textwrap.dedent("""\
    \t\treturn nil, πE
    \t})
    \tπg.RegisterModule($modname, Code)
    }"""), modname=util.go_str(modname))

  if pep3147:
    file_buffer.seek(0)
    honor_pep3147(script, file_buffer)

  file_buffer.seek(0)
  sys.stdout.writelines(file_buffer.readlines())
  return 0

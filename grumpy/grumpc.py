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

import importlib2

import grumpy
from grumpy.compiler import block
from grumpy.compiler import imputil
from grumpy.compiler import stmt
from grumpy.compiler import util
from grumpy.vendor import pythonparser

GOPATH_FOLDER = 'gopath'
GOPATH_PATTERN = 'src/__python__/'
GRUMPY_MAGIC_TAG = 'grumpy-' + grumpy.__version__.replace('.', '')  # alike cpython-27
ORIGINAL_MAGIC_TAG = sys.implementation.cache_tag  # On Py27, only because importlib2


def honor_pep3147(script_path, stream=None, only_makedirs=False):
  assert script_path.endswith('.py')

  script_basename = script_path.rpartition('.')[0].rpartition('/')[-1]

  ### TODO: Fix race conditions
  sys.implementation.cache_tag = GRUMPY_MAGIC_TAG
  cache_folder = os.path.abspath(os.path.normpath(
    importlib2._bootstrap.cache_from_source(script_path)
  ))
  sys.implementation.cache_tag = ORIGINAL_MAGIC_TAG
  ###

  gopath_folder = os.path.join(cache_folder, GOPATH_FOLDER)
  gopath_modules_folder = os.path.join(gopath_folder, GOPATH_PATTERN)
  module_folder = os.path.join(gopath_modules_folder, script_basename)

  for needed_folder in (cache_folder, gopath_folder, module_folder):
    if os.path.isfile(needed_folder):   # 1. Remove the file named as needed folder
      os.unlink(path)
    if not os.path.exists(needed_folder):   # 2. Create the needed folder
      os.makedirs(needed_folder)

  outputs = {
    'cache_folder': cache_folder,
    'gopath_folder': gopath_folder,
    'gopath_modules_folder': gopath_modules_folder,
    'module_folder': module_folder,
  }
  if only_makedirs:
    return outputs

  gopath_script_filename = os.path.normpath(os.path.join(
    module_folder, '..', script_basename + '.py'
  ))
  with open(gopath_script_filename, 'w') as gopath_script_file:
    with open(script_path) as original_file:
      gopath_script_file.writelines(original_file.readlines())

  module_filename = os.path.join(module_folder, 'module.go')
  with open(module_filename, 'w') as module_file:
    module_file.writelines(stream.readlines())
  return outputs


def main(script=None, modname='__main__', pep3147=False, extend_gopath=False):
  assert script and modname, 'Script "%s" or Modname "%s" is empty' % (script,modname)

  gopath = os.getenv('GOPATH', None)
  if not gopath:
    to_raise = RuntimeError('GOPATH not set')
    to_raise.exitcode = 1
    raise to_raise

  with open(script) as py_file:
    py_contents = py_file.read()
  try:
    mod = pythonparser.parse(py_contents)
  except SyntaxError as e:
    to_raise = RuntimeError('{}: line {}: invalid syntax: {}'.format(
        e.filename, e.lineno, e.text
    ))
    to_raise.exitcode = 2
    raise to_raise

  # Do a pass for compiler directives from `from __future__ import *` statements
  try:
    future_node, future_features = imputil.parse_future_features(mod)
  except util.CompileError as e:
    e.exitcode = 2
    raise

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
      e.exitcode = 2
      raise

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
    new_gopath = honor_pep3147(script, stream=file_buffer)['gopath_folder']
    if extend_gopath:
      gopath = gopath + os.pathsep + new_gopath
      os.environ['GOPATH'] = gopath
  else:
    file_buffer.seek(0)
    sys.stdout.writelines(file_buffer.readlines())

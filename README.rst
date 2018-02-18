============
Grumpy Tools
============


.. image:: https://img.shields.io/pypi/v/grumpy_tools.svg
        :target: https://pypi.python.org/pypi/grumpy_tools

.. image:: https://img.shields.io/travis/alanjds/grumpy_tools.svg
        :target: https://travis-ci.org/alanjds/grumpy_tools

.. image:: https://readthedocs.org/projects/grumpy-tools/badge/?version=latest
        :target: https://grumpy-tools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/alanjds/grumpy_tools/shield.svg
     :target: https://pyup.io/repos/github/alanjds/grumpy_tools/
     :alt: Updates



Python Tools needed by the Grumpy Transpiler & Runtime


* Free software: Apache Software License 2.0
* Documentation: https://grumpy-tools.readthedocs.io.


Quick Start
-----------

.. code-block:: bash

        pip install https://github.com/alanjds/grumpy-tools/archive/master.zip
        echo 'print("Hello World")' > hello.py
        grumpy transpile hello.py
        # Awe the Golang-transpiled code echoed to stdout!

Credits
-------

All the code cames from the Google Grumpy project. This is just a PoC trying to
provide a better CLI than the original one.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

================================
Parallel write
================================

.. image:: https://github.com/Mikata-Project/parallel_write/workflows/Tests/badge.svg?branch=master
    :target: https://github.com/Mikata-Project/parallel_write/actions?workflow=Tests
    :alt: Test Status

.. image:: https://github.com/Mikata-Project/parallel_write/workflows/Package%20Build/badge.svg?branch=master
    :target: https://github.com/Mikata-Project/parallel_write/actions?workflow=Package%20Build
    :alt: Package Build

.. image:: https://codecov.io/gh/Mikata-Project/parallel_write/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Mikata-Project/parallel_write
    :alt: Codecov

.. image:: https://img.shields.io/readthedocs/parallel-write/latest?label=Read%20the%20Docs
    :target: https://parallel-write.readthedocs.io/en/latest/index.html
    :alt: Read the Docs

Summary
=======

Parallel write is a Python module for distributing writes between an arbitrary number of open
file(like) objects.

Features:

* Distributes each calls to the proxy object to each passed file objects, so all of them
  should be in the same state
* Writes are done in a configurable length thread pool, so you can have slower underlying
  objects, their slowness won't add up
* Compares results from the methods, so despite its name, you can actually read from many objects
  at once and fail if any of them return different data

Motivation
==========

We often write the same data to local disk (for later caching) and remote (S3 for persistence).
The files must be the same, but the tool we're using may produce binary-different outputs for
two subsequent writes (either because `PYTHONHASH` shuffles things or it includes time-stamps
into the compressed output's metadata, doesn't matter).

We could write the file locally first, then copy it to S3, but that would take more time and
complexity in code. It's easier to write them at the same time.

How to use this module
======================

See the `documentation`_.


Issues and Discussions
======================

As usual in any GitHub based project, raise an `issue`_ if you find any bug or room for
improvements.

Version
=======

v0.0.8

.. _documentation: https://parallel-write.readthedocs.io/en/latest/
.. _issue: https://github.com/Mikata-Project/parallel_write/issues

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


long_description = '{}\n{}'.format(
    read('README.rst'),
    read(join('docs', 'CHANGELOG.rst')),
    )

setup(
    name='parallel_write',
    version='0.0.2',
    description='Writes to many open files in parallel.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='MIT License',
    author='NAGY, Attila',
    author_email='nagy.attila@gmail.com',
    url='https://github.com/Mikata-Project/parallel_write',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
    project_urls={
        'webpage': 'https://github.com/Mikata-Project/parallel_write',
        'Documentation': 'https://python-project-skeleton.readthedocs.io/en/latest/',
        'Changelog': 'https://github.com/Mikata-Project/parallel_write/blob/master/docs/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/Mikata-Project/parallel_write/issues',
        'Discussion Forum': 'https://github.com/Mikata-Project/parallel_write/discussions',
        },
    keywords=[
        'ci', 'continuous-integration', 'project-template',
        'project-skeleton', 'sample-project',
        # eg: 'keyword1', 'keyword2', 'keyword3',
        ],
    python_requires='>=3.5',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
        },
    setup_requires=[
        #   'pytest-runner',
        #   'setuptools_scm>=3.3.1',
        ],
    entry_points={},
    # cmdclass={'build_ext': optional_build_ext},
    # ext_modules=[
    #    Extension(
    #        splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
    #        sources=[path],
    #        include_dirs=[dirname(path)]
    #    )
    #    for root, _, _ in os.walk('src')
    #    for path in glob(join(root, '*.c'))
    # ],
    )

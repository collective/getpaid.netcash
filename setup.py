"""
$Id: setup.py 1868 2008-08-22 22:00:38Z fairwinds.dp $

Copyright (c) 2007 - 2008 ifPeople, Kapil Thangavelu, and Contributors
All rights reserved. Refer to LICENSE.txt for details of distribution and use.

Distutils setup
 
"""

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='getpaid.netcash',
    version='0.9dev',
    license = 'ZPL2.1',
    author='Hannes Calitz',
    author_email='hannes@opennetworks.co.za',
    description='Get paid NetCash payment processor functionality. Built on the VCS processor.',
    long_description = (),
    classifiers = [
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Framework :: Plone'
        ],
    url='http://code.google.com/p/getpaid',
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = ['setuptools',
                        'getpaid.core',
                        'zope.interface',
                        'zope.component',
                       ],
    zip_safe = False,
    )


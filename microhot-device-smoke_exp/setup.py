import os
from setuptools import setup

PYTHON_VERSION = '>=3.6.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


INSTALL_REQUIRES=[
    'behave',
    'allure-behave',
    'requests',
    'PyHamcrest',
    'pexpect',
    'requests_toolbelt'
]

setup(
    name='microhot-device-automation-suite',
    packages=['libs'],
    require_python=PYTHON_VERSION,
    install_requires=INSTALL_REQUIRES,
    description="BDD-style testing tool of micro-hot device",
    long_description=read('README.rst'),
    author='cguoqing',
    author_email='cguoqing@cewisec.com'
)
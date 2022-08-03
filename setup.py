from setuptools import find_packages, setup
import os

setup(
    name='pyisva',
    version='0.1.%s' % os.environ.get('TRAVIS_BUILD_NUMBER', 0),
    description='Python API for IBM Security Verify Access',
    author='Lachlan Gleeson',
    author_email='lgleeson@au1.ibm.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.23.0'
    ],
    url='https://github.ibm.com/ibm-security/pyisva',
    zip_safe=False
)

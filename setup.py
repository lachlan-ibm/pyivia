from setuptools import find_packages, setup
import os

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pyisva',
    version='0.2.%s' % os.environ.get('TRAVIS_BUILD_NUMBER', 0),
    description='Python API for IBM Security Verify Access',
    author='Lachlan Gleeson',
    author_email='lgleeson@au1.ibm.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.23.0'
    ],
    url='https://github.com/lachlan-ibm/pyisva',
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown'
)

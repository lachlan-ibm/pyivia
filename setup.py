from setuptools import find_packages, setup, Command
import os

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        for root, dirs, files in os.walk("./", topdown=False):
            for name in files:
                if name.endswith((".pyc", ".tgz", ".whl")):
                    print("remove {}".format(os.path.join(root, name)))
                    os.remove(os.path.join(root, name))
            for name in dirs:
                if name.endswith((".egg-info", "build", "dist", "__pycache__", "html")):
                    print("remove {}".format(os.path.join(root, name)))
                    #os.rmdir(os.path.join(root, name))
                    os.system('rm -vrf {}'.format(os.path.join(root, name)))

BUILD_ID = os.environ.get('TRAVIS_BUILD_NUMBER', 0)
if BUILD_ID == 0:
    BUILD_ID = os.environ.get('GITHUB_RUN_NUMBER', 0)

setup(
    name='pyivia',
    version='0.2.%s' % BUILD_ID,
    description='Python API for IBM Verify Identity Access',
    author='Lachlan Gleeson',
    author_email='lgleeson@au1.ibm.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.23.0'
    ],
    url='https://github.com/lachlan-ibm/pyivia',
    project_urls={
        'Homepage': 'https://github.com/lachlan-ibm/pyivia',
        'Documentation': 'https://lachlan-ibm.github.io/pyivia',
        'Source': 'https://github.com/lachlan-ibm/pyivia',
        'Tracker': 'https://github.com/lachlan-ibm/pyivia/issues'
    },
    zip_safe=False,
    cmdclass={
        'clean': CleanCommand,
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)

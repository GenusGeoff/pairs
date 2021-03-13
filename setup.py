
from setuptools import setup, find_packages
from pairs.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='pairs',
    version=VERSION,
    description='A CLI for evaluating pairs trades',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='def-mycroft (zero)',
    author_email='john.doe@example.com',
    url='https://github.com/def-mycroft/pairs',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'pairs': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        pairs = pairs.main:main
    """,
)

import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_oppwa import __version__


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}


setup(
    name='pretix-oppwa',
    version=__version__,
    description='This plugin allows you to use OPPWA based payment providers',
    long_description=long_description,
    url='https://github.com/pretix/pretix-oppwa/',
    author='Martin Gross',
    author_email='gross@rami.io',
    license='Apache',

    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_oppwa=pretix_oppwa:PretixPluginMeta
pretix_vrpay=pretix_vrpay:PretixPluginMeta
pretix_hobex=pretix_hobex:PretixPluginMeta
""",
)

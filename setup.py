from setuptools import setup, find_packages
from libbgp import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='libbgp',
    version=__version__,
    url='https://github.com/smartbgp/libbgp',
    license='Apache 2.0',
    author='Peng Xiao',
    author_email='xiaoquwl@gmail.com',
    keywords='BGP BMP Python',
    description='Python BGP/BMP Message parser lib',
    long_description=long_description,
    platforms='any',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)

from setuptools import find_packages
from setuptools import setup


def read(filename):
    with open(filename, "r") as fh:
        return fh.read()


setup(
    name="mrsr",
    version="0.0.5",
    url="https://github.com/omadson/mrsr",
    license='MIT',

    author="Madson Dias",
    author_email="madsonddias@gmail.com",

    description="A simple implementation of the multiresponse sparse regression (MRSR) algorithm.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",

    packages=find_packages(exclude=('tests',)),

    install_requires=[
        'numpy>=1.15.4'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

from setuptools import setup
from setuptools import find_packages

setup(
    name='cliffdemo',
    version='0.1',
    install_requires=['cliff'],
    namespace_packages=[],
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'cliffdemo = cliffdemo.main:main'
        ],
        'cliff.demo': [
          'simple = cliffdemo.simple:Simple',
        ],
    }
)

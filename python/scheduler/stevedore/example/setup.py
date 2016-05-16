from setuptools import setup, find_packages
setup(
    entry_points={
        'stevedore.example.formatter': [
            'simple = stevedore.example.simple:Simple',
            'field = stevedore.example.fields:FieldList',
            'plain = stevedore.example.simple:Simple',
        ],
    },
)
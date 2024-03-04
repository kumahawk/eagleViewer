from setuptools import setup

setup(
    name='eagleviewer',
    packages=['eagleviewer'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'requests',
    ],
)